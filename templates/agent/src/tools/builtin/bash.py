"""Bash tool — execute shell commands.

Mirrors Claude Code's Bash tool with permission-aware command classification.
"""

from __future__ import annotations

import asyncio
import shlex
from typing import Any

from src.tools.base import Tool
from src.types import PermissionBehavior, PermissionResult, ToolResult

# Commands considered safe (read-only)
SAFE_PREFIXES = [
    "ls", "cat", "head", "tail", "wc", "echo", "pwd", "whoami", "date",
    "git status", "git log", "git diff", "git branch", "git show",
    "find", "grep", "rg", "which", "type", "file", "stat",
    "python --version", "node --version", "npm --version",
]

# Commands that are destructive
DESTRUCTIVE_PATTERNS = [
    "rm -rf", "rm -r /", "sudo rm", "mkfs", "> /dev/",
    "dd if=", "chmod -R 777", "curl | sh", "wget | sh",
]


class BashTool(Tool):
    @property
    def name(self) -> str:
        return "bash"

    @property
    def description(self) -> str:
        return (
            "Execute a bash command and return its output. "
            "Use this for running shell commands, scripts, git operations, etc. "
            "Commands run in the current working directory."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The bash command to execute",
                },
                "timeout": {
                    "type": "integer",
                    "description": "Timeout in seconds (default 120)",
                    "default": 120,
                },
            },
            "required": ["command"],
        }

    @property
    def is_destructive(self) -> bool:
        return True  # bash can do anything

    def check_permissions(self, args: dict[str, Any]) -> PermissionResult:
        cmd = args.get("command", "").strip()
        # Check if it's a known safe command
        for prefix in SAFE_PREFIXES:
            if cmd.startswith(prefix):
                return PermissionResult(behavior=PermissionBehavior.ALLOW, reason=f"Safe command: {prefix}")
        # Check if it's explicitly destructive
        for pattern in DESTRUCTIVE_PATTERNS:
            if pattern in cmd:
                return PermissionResult(behavior=PermissionBehavior.DENY, reason=f"Destructive pattern: {pattern}")
        # Otherwise defer to general permission system
        return PermissionResult(behavior=PermissionBehavior.ASK, reason="Non-trivial bash command")

    async def execute(self, args: dict[str, Any]) -> ToolResult:
        command = args["command"]
        timeout = args.get("timeout", 120)

        try:
            proc = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            output_parts = []
            if stdout:
                output_parts.append(stdout.decode(errors="replace"))
            if stderr:
                output_parts.append(f"[stderr]\n{stderr.decode(errors='replace')}")
            output = "\n".join(output_parts) or "(no output)"

            if proc.returncode != 0:
                output = f"Exit code: {proc.returncode}\n{output}"

            # Truncate very long output
            if len(output) > 50_000:
                output = output[:50_000] + "\n... (output truncated)"

            return ToolResult(output=output, is_error=proc.returncode != 0)

        except asyncio.TimeoutError:
            return ToolResult(output=f"Command timed out after {timeout}s", is_error=True)
        except Exception as e:
            return ToolResult(output=f"Error executing command: {e}", is_error=True)
