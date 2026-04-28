"""Tool registry — single source of truth for all available tools.

Mirrors Claude Code's tools.ts: getAllBaseTools() + assembleToolPool().
"""

from __future__ import annotations

from typing import Any

from src.tools.base import Tool


class ToolRegistry:
    """Central registry for all tools. Supports dynamic registration."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def all(self) -> list[Tool]:
        return list(self._tools.values())

    def names(self) -> list[str]:
        return list(self._tools.keys())

    def to_llm_schemas(self) -> list[dict[str, Any]]:
        """Export all tools as LLM function-calling schemas."""
        return [t.to_llm_schema() for t in self._tools.values()]

    def read_only_tools(self) -> list[Tool]:
        return [t for t in self._tools.values() if t.is_read_only]


# ---------------------------------------------------------------------------
# Singleton with all built-in tools pre-registered
# ---------------------------------------------------------------------------

_registry: ToolRegistry | None = None


def get_tool_registry() -> ToolRegistry:
    global _registry
    if _registry is None:
        _registry = _build_default_registry()
    return _registry


def _build_default_registry() -> ToolRegistry:
    """Register all built-in tools. Add your custom tools here."""
    from src.tools.builtin.bash import BashTool
    from src.tools.builtin.read_file import ReadFileTool
    from src.tools.builtin.write_file import WriteFileTool
    from src.tools.builtin.edit_file import EditFileTool
    from src.tools.builtin.glob_tool import GlobTool
    from src.tools.builtin.grep_tool import GrepTool
    from src.tools.builtin.web_fetch import WebFetchTool
    from src.tools.builtin.agent_tool import SubAgentTool
    from src.tools.builtin.ask_user import AskUserTool

    registry = ToolRegistry()
    for tool in [
        BashTool(),
        ReadFileTool(),
        WriteFileTool(),
        EditFileTool(),
        GlobTool(),
        GrepTool(),
        WebFetchTool(),
        SubAgentTool(),
        AskUserTool(),
    ]:
        registry.register(tool)
    return registry
