"""Sub-agent tool — spawn a child agent for complex sub-tasks.

Mirrors Claude Code's AgentTool: the main agent can delegate work to sub-agents,
each with its own conversation history, tool access, and iteration limit.
"""

from __future__ import annotations

from typing import Any

from src.tools.base import Tool
from src.types import ToolResult


class SubAgentTool(Tool):
    @property
    def name(self) -> str:
        return "sub_agent"

    @property
    def description(self) -> str:
        return (
            "Spawn a sub-agent to handle a complex sub-task autonomously. "
            "The sub-agent has its own conversation and tool access. "
            "Use this for tasks that require multiple steps or deep exploration, "
            "so the main conversation stays focused."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": "Detailed description of the task for the sub-agent",
                },
                "model": {
                    "type": "string",
                    "description": "Optional model override for the sub-agent",
                },
            },
            "required": ["task"],
        }

    async def execute(self, args: dict[str, Any]) -> ToolResult:
        """Spawn a sub-agent loop and collect the final result."""
        from src.engine.agent_loop import AgentLoop
        from src.permissions.checker import PermissionChecker
        from src.tools.registry import get_tool_registry

        task = args["task"]
        model = args.get("model")

        # Create a child agent with reduced iteration limit
        child = AgentLoop(
            registry=get_tool_registry(),
            permission_checker=PermissionChecker(),
            model=model,
            max_iterations=10,
            system_prompt=(
                "You are a sub-agent working on a specific task. "
                "Complete the task thoroughly, then provide a clear summary of what you did and found."
            ),
        )

        # Run the child agent and collect the final response
        from src.engine.agent_loop import EventType

        final_content = ""
        async for event in child.run(task):
            if event.type == EventType.ASSISTANT_MESSAGE:
                final_content = event.data.get("content", "")
            elif event.type == EventType.DONE:
                final_content = event.data.get("content", "") or final_content

        return ToolResult(output=final_content or "(sub-agent produced no output)")
