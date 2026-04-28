"""Edit file tool — find-and-replace within a file."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.tools.base import Tool
from src.types import ToolResult


class EditFileTool(Tool):
    @property
    def name(self) -> str:
        return "edit_file"

    @property
    def description(self) -> str:
        return (
            "Edit a file by replacing an exact string with a new string. "
            "The old_string must match exactly (including whitespace/indentation). "
            "Use replace_all=true to replace all occurrences."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Path to the file to edit"},
                "old_string": {"type": "string", "description": "Exact string to find"},
                "new_string": {"type": "string", "description": "String to replace it with"},
                "replace_all": {"type": "boolean", "description": "Replace all occurrences", "default": False},
            },
            "required": ["file_path", "old_string", "new_string"],
        }

    def validate_input(self, args: dict[str, Any]) -> str | None:
        path = Path(args.get("file_path", ""))
        if not path.exists():
            return f"File not found: {path}"
        if args.get("old_string") == args.get("new_string"):
            return "old_string and new_string are identical"
        return None

    async def execute(self, args: dict[str, Any]) -> ToolResult:
        path = Path(args["file_path"])
        old = args["old_string"]
        new = args["new_string"]
        replace_all = args.get("replace_all", False)

        try:
            content = path.read_text()
            count = content.count(old)
            if count == 0:
                return ToolResult(output="old_string not found in file. Check whitespace and indentation.", is_error=True)
            if count > 1 and not replace_all:
                return ToolResult(
                    output=f"old_string found {count} times. Use replace_all=true or provide more context to make it unique.",
                    is_error=True,
                )
            if replace_all:
                new_content = content.replace(old, new)
            else:
                new_content = content.replace(old, new, 1)
            path.write_text(new_content)
            replaced = count if replace_all else 1
            return ToolResult(output=f"Replaced {replaced} occurrence(s) in {path}")
        except Exception as e:
            return ToolResult(output=f"Error editing file: {e}", is_error=True)
