"""Write file tool — create or overwrite a file."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.tools.base import Tool
from src.types import ToolResult


class WriteFileTool(Tool):
    @property
    def name(self) -> str:
        return "write_file"

    @property
    def description(self) -> str:
        return "Create a new file or completely overwrite an existing file with the provided content."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Path to write the file"},
                "content": {"type": "string", "description": "Content to write to the file"},
            },
            "required": ["file_path", "content"],
        }

    async def execute(self, args: dict[str, Any]) -> ToolResult:
        path = Path(args["file_path"])
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(args["content"])
            return ToolResult(output=f"File written: {path} ({len(args['content'])} chars)")
        except Exception as e:
            return ToolResult(output=f"Error writing file: {e}", is_error=True)
