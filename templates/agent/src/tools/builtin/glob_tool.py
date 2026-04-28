"""Glob tool — find files by pattern."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.tools.base import Tool
from src.types import ToolResult


class GlobTool(Tool):
    @property
    def name(self) -> str:
        return "glob"

    @property
    def description(self) -> str:
        return "Find files matching a glob pattern (e.g. '**/*.py', 'src/**/*.ts'). Returns matching file paths."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "Glob pattern to match files"},
                "path": {"type": "string", "description": "Directory to search in (default: current directory)", "default": "."},
            },
            "required": ["pattern"],
        }

    @property
    def is_read_only(self) -> bool:
        return True

    async def execute(self, args: dict[str, Any]) -> ToolResult:
        pattern = args["pattern"]
        base = Path(args.get("path", "."))

        try:
            matches = sorted(base.glob(pattern))
            if not matches:
                return ToolResult(output=f"No files matched pattern: {pattern}")
            # Limit output
            output_lines = [str(m) for m in matches[:500]]
            output = "\n".join(output_lines)
            if len(matches) > 500:
                output += f"\n... ({len(matches) - 500} more files)"
            return ToolResult(output=output)
        except Exception as e:
            return ToolResult(output=f"Error in glob: {e}", is_error=True)
