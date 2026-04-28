"""Unit tests for built-in tools."""

import pytest
from pathlib import Path

from src.tools.builtin.read_file import ReadFileTool
from src.tools.builtin.write_file import WriteFileTool
from src.tools.builtin.edit_file import EditFileTool
from src.tools.builtin.glob_tool import GlobTool
from src.tools.builtin.grep_tool import GrepTool


@pytest.fixture
def tmp_file(tmp_path: Path) -> Path:
    f = tmp_path / "test.txt"
    f.write_text("line 1\nline 2\nline 3\n")
    return f


@pytest.mark.asyncio
async def test_read_file(tmp_file: Path):
    tool = ReadFileTool()
    result = await tool.execute({"file_path": str(tmp_file)})
    assert not result.is_error
    assert "line 1" in result.output
    assert "line 3" in result.output


@pytest.mark.asyncio
async def test_read_file_not_found():
    tool = ReadFileTool()
    err = tool.validate_input({"file_path": "/nonexistent/file.txt"})
    assert err is not None
    assert "not found" in err


@pytest.mark.asyncio
async def test_write_file(tmp_path: Path):
    tool = WriteFileTool()
    target = tmp_path / "new_file.txt"
    result = await tool.execute({"file_path": str(target), "content": "hello world"})
    assert not result.is_error
    assert target.read_text() == "hello world"


@pytest.mark.asyncio
async def test_edit_file(tmp_file: Path):
    tool = EditFileTool()
    result = await tool.execute({
        "file_path": str(tmp_file),
        "old_string": "line 2",
        "new_string": "LINE TWO",
    })
    assert not result.is_error
    assert "LINE TWO" in tmp_file.read_text()


@pytest.mark.asyncio
async def test_edit_file_not_found_string(tmp_file: Path):
    tool = EditFileTool()
    result = await tool.execute({
        "file_path": str(tmp_file),
        "old_string": "nonexistent string",
        "new_string": "replacement",
    })
    assert result.is_error


@pytest.mark.asyncio
async def test_glob(tmp_path: Path):
    (tmp_path / "a.py").write_text("")
    (tmp_path / "b.py").write_text("")
    (tmp_path / "c.txt").write_text("")
    tool = GlobTool()
    result = await tool.execute({"pattern": "*.py", "path": str(tmp_path)})
    assert not result.is_error
    assert "a.py" in result.output
    assert "b.py" in result.output
    assert "c.txt" not in result.output


@pytest.mark.asyncio
async def test_grep(tmp_path: Path):
    (tmp_path / "file.py").write_text("def hello():\n    return 'world'\n")
    tool = GrepTool()
    result = await tool.execute({"pattern": "hello", "path": str(tmp_path), "file_pattern": "*.py"})
    assert not result.is_error
    assert "hello" in result.output
