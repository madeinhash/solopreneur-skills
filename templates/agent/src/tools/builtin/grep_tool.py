"""Grep tool — search file contents by pattern."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from src.tools.base import Tool
from src.types import ToolResult


class GrepTool(Tool):
    @property
    def name(self) -> str:
        return "grep"

    @property
    def description(self) -> str:
        return (
            "Search for a pattern in file contents. Supports regex. "
            "Returns matching lines with file paths and line numbers."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "Search pattern (regex supported)"},
                "path": {"type": "string", "description": "Directory or file to search", "default": "."},
                "file_pattern": {"type": "string", "description": "Glob to filter files (e.g. '*.py')", "default": "**/*"},
            },
            "required": ["pattern"],
        }

    @property
    def is_read_only(self) -> bool:
        return True

    async def execute(self, args: dict[str, Any]) -> ToolResult:
        pattern = args["pattern"]
        base = Path(args.get("path", "."))
        file_pattern = args.get("file_pattern", "**/*")

        try:
            regex = re.compile(pattern, re.IGNORECASE)
        except re.error as e:
            return ToolResult(output=f"Invalid regex: {e}", is_error=True)

        results: list[str] = []
        files = [base] if base.is_file() else sorted(base.glob(file_pattern))

        for fpath in files:
            if not fpath.is_file():
                continue
            try:
                for i, line in enumerate(fpath.read_text(errors="replace").splitlines(), 1):
                    if regex.search(line):
                        results.append(f"{fpath}:{i}: {line.rstrip()}")
                        if len(results) >= 200:
                            results.append("... (results truncated at 200 matches)")
                            return ToolResult(output="\n".join(results))
            except (PermissionError, OSError):
                continue

        if not results:
            return ToolResult(output=f"No matches for pattern: {pattern}")
        return ToolResult(output="\n".join(results))
