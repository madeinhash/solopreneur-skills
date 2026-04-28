"""Core type definitions — mirrors Claude Code's type system."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ---------------------------------------------------------------------------
# Messages — the universal message format flowing through the agent loop
# ---------------------------------------------------------------------------

class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


@dataclass
class Message:
    role: Role
    content: str
    tool_call_id: str | None = None
    tool_calls: list[ToolCall] | None = None
    name: str | None = None  # tool name for role=tool


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------

class PermissionBehavior(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    ASK = "ask"


@dataclass
class PermissionResult:
    behavior: PermissionBehavior
    reason: str = ""


@dataclass
class ToolResult:
    """Result returned by a tool execution."""
    output: str
    is_error: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Permission rules
# ---------------------------------------------------------------------------

@dataclass
class PermissionRule:
    tool_name: str          # e.g. "bash", "*" for all
    pattern: str = "*"      # e.g. "git *", "rm *"
    behavior: PermissionBehavior = PermissionBehavior.ASK
    source: str = "settings"  # "settings", "session", "cli"
