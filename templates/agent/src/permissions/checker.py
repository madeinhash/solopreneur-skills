"""Permission system — mirrors Claude Code's multi-stage permission pipeline.

Decision flow:
1. Tool.validate_input()   — reject malformed input
2. Tool.check_permissions() — tool-specific rules (e.g. bash command classification)
3. PermissionChecker.check() — general rules engine (allow/deny/ask rules)
4. Permission mode fallback  — ask/auto/strict
"""

from __future__ import annotations

import fnmatch
from typing import Any

from src.config import settings
from src.logger import logger
from src.tools.base import Tool
from src.types import PermissionBehavior, PermissionResult, PermissionRule


class PermissionChecker:
    """Rule-based permission checker with configurable mode."""

    def __init__(self) -> None:
        self.allow_rules: list[PermissionRule] = []
        self.deny_rules: list[PermissionRule] = []
        self._load_default_rules()

    def _load_default_rules(self) -> None:
        """Load sensible defaults. Users can add more via add_rule()."""
        # Deny destructive bash patterns by default
        for pattern in ["rm -rf *", "rm -r /*", "sudo rm *", "mkfs *", "> /dev/*"]:
            self.deny_rules.append(
                PermissionRule(tool_name="bash", pattern=pattern, behavior=PermissionBehavior.DENY, source="default")
            )

    def add_rule(self, rule: PermissionRule) -> None:
        if rule.behavior == PermissionBehavior.ALLOW:
            self.allow_rules.append(rule)
        elif rule.behavior == PermissionBehavior.DENY:
            self.deny_rules.append(rule)

    def check(self, tool: Tool, args: dict[str, Any]) -> PermissionResult:
        """Multi-stage permission check."""
        # Stage 1: Input validation
        validation_error = tool.validate_input(args)
        if validation_error:
            return PermissionResult(behavior=PermissionBehavior.DENY, reason=f"Invalid input: {validation_error}")

        # Stage 2: Tool-specific permission logic
        tool_permission = tool.check_permissions(args)
        if tool_permission.behavior != PermissionBehavior.ALLOW:
            return tool_permission

        # Stage 3: Read-only tools always allowed
        if tool.is_read_only:
            return PermissionResult(behavior=PermissionBehavior.ALLOW, reason="read-only tool")

        # Stage 4: Check deny rules (deny rules take priority)
        match_key = self._get_match_key(tool, args)
        for rule in self.deny_rules:
            if self._rule_matches(rule, tool.name, match_key):
                logger.warn("permission_denied", tool=tool.name, rule=rule.pattern, source=rule.source)
                return PermissionResult(behavior=PermissionBehavior.DENY, reason=f"Denied by rule: {rule.pattern}")

        # Stage 5: Check allow rules
        for rule in self.allow_rules:
            if self._rule_matches(rule, tool.name, match_key):
                return PermissionResult(behavior=PermissionBehavior.ALLOW, reason=f"Allowed by rule: {rule.pattern}")

        # Stage 6: Fall back to permission mode
        mode = settings.permission_mode
        if mode == "auto":
            return PermissionResult(behavior=PermissionBehavior.ALLOW, reason="auto mode")
        elif mode == "strict":
            return PermissionResult(behavior=PermissionBehavior.DENY, reason="strict mode — not explicitly allowed")
        else:  # "ask"
            return PermissionResult(behavior=PermissionBehavior.ASK, reason="requires user approval")

    def _get_match_key(self, tool: Tool, args: dict[str, Any]) -> str:
        """Extract the key string to match against rules."""
        if tool.name == "bash":
            return args.get("command", "")
        return str(args)

    def _rule_matches(self, rule: PermissionRule, tool_name: str, match_key: str) -> bool:
        """Check if a rule matches the tool + input."""
        if rule.tool_name != "*" and rule.tool_name != tool_name:
            return False
        return fnmatch.fnmatch(match_key, rule.pattern)
