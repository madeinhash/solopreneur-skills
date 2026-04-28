"""Read file tool — read file contents with optional line range."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.tools.base import Tool
from src.types import ToolResult


class ReadFileTool(Tool):
    @property
    def name(self) -> str:
        return "read_file"

    @property
    def description(self) -> str:
        return (
            "Read the contents of a file. Returns the file content with line numbers. "
            "Use offset and limit to read specific portions of large files."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Path to the file to read"},
                "offset": {"type": "integer", "description": "Line number to start from (1-based)", "default": 1},
                "limit": {"type": "integer", "description": "Max number of lines to read", "default": 2000},
            },
            "required": ["file_path"],
        }

    @property
    def is_read_only(self) -> bool:
        return True

    def validate_input(self, args: dict[str, Any]) -> str | None:
        path = Path(args.get("file_path", ""))
        if not path.exists():
            return f"File not found: {path}"
        if path.is_dir():
            return f"Path is a directory, not a file: {path}"
        return None

    async def execute(self, args: dict[str, Any]) -> ToolResult:
        path = Path(args["file_path"])
        offset = max(1, args.get("offset", 1))
        limit = args.get("limit", 2000)

        try:
            lines = path.read_text(errors="replace").splitlines()
            total = len(lines)
            selected = lines[offset - 1 : offset - 1 + limit]
            numbered = [f"{offset + i:>6}\t{line}" for i, line in enumerate(selected)]
            output = "\n".join(numbered)
            if offset + limit - 1 < total:
                output += f"\n\n... ({total - offset - limit + 1} more lines)"
            return ToolResult(output=output or "(empty file)")
        except Exception as e:
            return ToolResult(output=f"Error reading file: {e}", is_error=True)
