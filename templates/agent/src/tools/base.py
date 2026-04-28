"""Base Tool class — all tools inherit from this.

Mirrors Claude Code's Tool pattern:
- Each tool has a name, description, input schema (for LLM), and execution logic
- Tools declare safety properties: is_read_only, is_destructive
- Tools can validate input and check permissions before execution
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from src.types import PermissionBehavior, PermissionResult, ToolResult


class Tool(ABC):
    """Base class for all agent tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique tool name (e.g. 'bash', 'read_file')."""

    @property
    @abstractmethod
    def description(self) -> str:
        """Description shown to the LLM — explain when and how to use this tool."""

    @property
    @abstractmethod
    def parameters(self) -> dict[str, Any]:
        """JSON Schema for tool parameters (sent to LLM as function schema)."""

    # --- Safety descriptors (fail-closed defaults like Claude Code) ---

    @property
    def is_read_only(self) -> bool:
        """Read-only tools can run concurrently. Default: False (conservative)."""
        return False

    @property
    def is_destructive(self) -> bool:
        """Destructive tools require explicit permission. Default: False."""
        return False

    # --- Lifecycle hooks ---

    def validate_input(self, args: dict[str, Any]) -> str | None:
        """Validate input before permission check. Return error message or None."""
        return None

    def check_permissions(self, args: dict[str, Any]) -> PermissionResult:
        """Tool-specific permission logic. Called before the general permission system.

        Override this for tools that need fine-grained rules
        (e.g. bash: allow 'git status' but ask for 'rm -rf').
        """
        return PermissionResult(behavior=PermissionBehavior.ALLOW)

    @abstractmethod
    async def execute(self, args: dict[str, Any]) -> ToolResult:
        """Execute the tool and return a result."""

    # --- LLM schema export ---

    def to_llm_schema(self) -> dict[str, Any]:
        """Export as LLM function-calling schema (OpenAI format)."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }
