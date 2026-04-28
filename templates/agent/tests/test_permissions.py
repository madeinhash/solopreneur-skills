"""Unit tests for the permission system."""

from src.permissions.checker import PermissionChecker
from src.tools.builtin.bash import BashTool
from src.tools.builtin.read_file import ReadFileTool
from src.types import PermissionBehavior


def test_read_only_always_allowed():
    checker = PermissionChecker()
    tool = ReadFileTool()
    result = checker.check(tool, {"file_path": "/etc/passwd"})
    assert result.behavior == PermissionBehavior.ALLOW


def test_bash_safe_command_allowed():
    checker = PermissionChecker()
    tool = BashTool()
    result = checker.check(tool, {"command": "git status"})
    assert result.behavior == PermissionBehavior.ALLOW


def test_bash_destructive_denied():
    checker = PermissionChecker()
    tool = BashTool()
    result = checker.check(tool, {"command": "rm -rf /"})
    assert result.behavior == PermissionBehavior.DENY
