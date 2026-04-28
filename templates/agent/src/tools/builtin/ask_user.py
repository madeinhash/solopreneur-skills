"""Ask user tool — request clarification or input from the user."""

from __future__ import annotations

from typing import Any

from src.tools.base import Tool
from src.types import ToolResult


class AskUserTool(Tool):
    @property
    def name(self) -> str:
        return "ask_user"

    @property
    def description(self) -> str:
        return (
            "Ask the user a question when you need clarification or more information. "
            "The user's response will be returned. Use this instead of guessing."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "The question to ask the user"},
            },
            "required": ["question"],
        }

    @property
    def is_read_only(self) -> bool:
        return True

    async def execute(self, args: dict[str, Any]) -> ToolResult:
        # In API mode, this returns the question as output.
        # The CLI overrides this with interactive input.
        question = args["question"]
        return ToolResult(output=f"[Pending user response to: {question}]")
