"""Agent Loop — the core execution engine.

Mirrors Claude Code's query.ts loop:
  LLM call → parse tool calls → check permissions → execute tools → feed results → repeat

Key design:
- Async generator: yields events (messages, tool calls, results) for streaming to UI/API
- Concurrency: read-only tools run in parallel, write tools run serially
- Permission gating: every tool call goes through the permission checker
- Iteration limit: prevents runaway loops
"""

from __future__ import annotations

import asyncio
import json
import uuid
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, AsyncGenerator

from src.config import settings
from src.engine.llm import chat_completion
from src.logger import logger
from src.permissions.checker import PermissionChecker
from src.tools.base import Tool
from src.tools.registry import ToolRegistry
from src.types import PermissionBehavior, ToolResult


# ---------------------------------------------------------------------------
# Event types yielded by the agent loop (for streaming to CLI/API)
# ---------------------------------------------------------------------------

class EventType(str, Enum):
    ASSISTANT_MESSAGE = "assistant_message"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    PERMISSION_REQUEST = "permission_request"
    ERROR = "error"
    DONE = "done"


@dataclass
class AgentEvent:
    type: EventType
    data: dict[str, Any]


# ---------------------------------------------------------------------------
# Permission callback — lets the host (CLI/API) handle "ask" behavior
# ---------------------------------------------------------------------------

# Default: auto-approve (for API mode). CLI overrides this with interactive prompt.
async def _default_permission_callback(tool_name: str, args: dict[str, Any], reason: str) -> bool:
    return True


PermissionCallback = type(_default_permission_callback)


# ---------------------------------------------------------------------------
# Agent Loop
# ---------------------------------------------------------------------------

class AgentLoop:
    """Core agent loop: LLM → tool calls → results → repeat.

    Usage:
        loop = AgentLoop(registry, permission_checker)
        async for event in loop.run("What files are in this directory?"):
            print(event)
    """

    def __init__(
        self,
        registry: ToolRegistry,
        permission_checker: PermissionChecker,
        *,
        model: str | None = None,
        max_iterations: int | None = None,
        system_prompt: str | None = None,
        permission_callback: PermissionCallback | None = None,  # type: ignore[assignment]
    ) -> None:
        self.registry = registry
        self.permission_checker = permission_checker
        self.model = model or settings.llm_model
        self.max_iterations = max_iterations or settings.agent_max_iterations
        self.system_prompt = system_prompt or self._load_system_prompt()
        self.permission_callback = permission_callback or _default_permission_callback
        self.messages: list[dict[str, Any]] = []

    def _load_system_prompt(self) -> str:
        path = settings.project_root / settings.agent_system_prompt_file
        if path.exists():
            return path.read_text()
        return "You are a helpful AI assistant with access to tools. Use them to complete tasks."

    async def run(
        self,
        user_message: str,
        *,
        session_messages: list[dict[str, Any]] | None = None,
    ) -> AsyncGenerator[AgentEvent, None]:
        """Run the agent loop. Yields events for each step.

        Args:
            user_message: The user's input
            session_messages: Optional existing conversation history for multi-turn
        """
        # Initialize messages
        if session_messages is not None:
            self.messages = list(session_messages)
        if not self.messages or self.messages[0].get("role") != "system":
            self.messages.insert(0, {"role": "system", "content": self.system_prompt})
        self.messages.append({"role": "user", "content": user_message})

        tool_schemas = self.registry.to_llm_schemas()
        iteration = 0

        while iteration < self.max_iterations:
            iteration += 1
            logger.info("agent_loop_iteration", iteration=iteration, max=self.max_iterations)

            # --- LLM call ---
            response = await chat_completion(self.messages, tools=tool_schemas, model=self.model)
            choice = response.choices[0]  # type: ignore[union-attr]
            message = choice.message

            # Append assistant message to history
            self.messages.append(message.model_dump())

            # --- Text response ---
            if message.content:
                yield AgentEvent(type=EventType.ASSISTANT_MESSAGE, data={"content": message.content})

            # --- No tool calls = done ---
            if not message.tool_calls:
                yield AgentEvent(type=EventType.DONE, data={
                    "content": message.content or "",
                    "iterations": iteration,
                })
                return

            # --- Execute tool calls ---
            tool_results = await self._execute_tool_calls(message.tool_calls)
            for tc, result in tool_results:
                yield AgentEvent(type=EventType.TOOL_CALL, data={
                    "tool": tc.function.name,
                    "arguments": json.loads(tc.function.arguments),
                })
                yield AgentEvent(type=EventType.TOOL_RESULT, data={
                    "tool": tc.function.name,
                    "tool_call_id": tc.id,
                    "output": result.output,
                    "is_error": result.is_error,
                })
                # Add tool result to message history
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result.output,
                })

        # Hit iteration limit
        yield AgentEvent(type=EventType.ERROR, data={
            "error": f"Reached max iterations ({self.max_iterations})",
        })
        yield AgentEvent(type=EventType.DONE, data={"content": "", "iterations": self.max_iterations})

    async def _execute_tool_calls(self, tool_calls: list[Any]) -> list[tuple[Any, ToolResult]]:
        """Execute tool calls with permission checking and concurrency control.

        Read-only tools run in parallel, write tools run serially.
        """
        # Partition into read-only and write groups
        read_only_calls: list[tuple[Any, Tool, dict[str, Any]]] = []
        write_calls: list[tuple[Any, Tool, dict[str, Any]]] = []

        for tc in tool_calls:
            tool = self.registry.get(tc.function.name)
            args = json.loads(tc.function.arguments)
            if tool is None:
                write_calls.append((tc, _UnknownTool(tc.function.name), args))
            elif tool.is_read_only:
                read_only_calls.append((tc, tool, args))
            else:
                write_calls.append((tc, tool, args))

        results: list[tuple[Any, ToolResult]] = []

        # Run read-only tools concurrently
        if read_only_calls:
            async def _run(item: tuple[Any, Tool, dict[str, Any]]) -> tuple[Any, ToolResult]:
                tc, tool, args = item
                return tc, await self._run_single_tool(tool, args)

            concurrent_results = await asyncio.gather(*[_run(item) for item in read_only_calls])
            results.extend(concurrent_results)

        # Run write tools serially
        for tc, tool, args in write_calls:
            result = await self._run_single_tool(tool, args)
            results.append((tc, result))

        return results

    async def _run_single_tool(self, tool: Tool, args: dict[str, Any]) -> ToolResult:
        """Run a single tool with permission checking."""
        # Permission check
        perm = self.permission_checker.check(tool, args)

        if perm.behavior == PermissionBehavior.DENY:
            logger.warn("tool_denied", tool=tool.name, reason=perm.reason)
            return ToolResult(output=f"Permission denied: {perm.reason}", is_error=True)

        if perm.behavior == PermissionBehavior.ASK:
            approved = await self.permission_callback(tool.name, args, perm.reason)
            if not approved:
                return ToolResult(output="User denied permission for this tool call.", is_error=True)

        # Execute
        try:
            logger.info("tool_execute", tool=tool.name, args_keys=list(args.keys()))
            result = await tool.execute(args)
            logger.info("tool_complete", tool=tool.name, is_error=result.is_error, output_len=len(result.output))
            return result
        except Exception as e:
            logger.error("tool_error", tool=tool.name, error=str(e))
            return ToolResult(output=f"Tool execution error: {e}", is_error=True)


class _UnknownTool(Tool):
    """Placeholder for tools the LLM hallucinated."""

    def __init__(self, tool_name: str) -> None:
        self._name = tool_name

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return ""

    @property
    def parameters(self) -> dict[str, Any]:
        return {}

    async def execute(self, args: dict[str, Any]) -> ToolResult:
        return ToolResult(output=f"Unknown tool: {self._name}. Available tools: use only the provided tools.", is_error=True)
