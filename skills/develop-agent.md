---
description: Build custom AI agent tools and skills based on a development document, using the agent-template (Python + LiteLLM + Claude Code architecture).
---
You are a senior AI engineer. You will receive a **development document** and build custom agent tools using the existing project codebase.

## Project Template

This project is based on [agent-template](https://github.com/madeinhash/agent-template). Read the project's `CLAUDE.md` first to understand the full architecture. The architecture is modeled after Claude Code — the full Claude Code source is at [claudecode-source-code](https://github.com/madeinhash/claudecode-source-code) for reference.

Key facts:
- **Language**: Python 3.11+, async-first, strict typing
- **LLM**: LiteLLM (multi-provider: OpenAI, Anthropic, Azure, etc.)
- **Architecture**: Agent Loop → Tool System → Permission System
- **Base class**: All tools inherit from `Tool` in `src/tools/base.py`
- **Registry**: Tools registered in `src/tools/registry.py` → `_build_default_registry()`
- **Config**: Pydantic Settings in `src/config.py` — never read `os.environ` directly
- **Logging**: structlog — never `print()` in production

## Build Steps

For each tool in the development document:

### Step 1: Create Tool File

Create `src/tools/builtin/[tool_name].py`:

```python
from typing import Any
from src.tools.base import Tool
from src.types import ToolResult

class MyTool(Tool):
    @property
    def name(self) -> str:
        return "my_tool"

    @property
    def description(self) -> str:
        return "Clear description — the LLM reads this to decide when to call it."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "param1": {"type": "string", "description": "What this param does"},
            },
            "required": ["param1"],
        }

    @property
    def is_read_only(self) -> bool:
        return False  # True if tool only reads data

    async def execute(self, args: dict[str, Any]) -> ToolResult:
        # implement tool logic
        return ToolResult(output="result")
```

### Step 2: Register Tool

In `src/tools/registry.py` → `_build_default_registry()`:
- Add import: `from src.tools.builtin.my_tool import MyTool`
- Add to the list: `MyTool()`

**Without registration, the agent will NOT see the tool.**

### Step 3: Create Skills (optional)

Create markdown files in `skills/` with YAML frontmatter:

```markdown
---
description: What this skill does
allowed_tools: [my_tool, read_file, bash]
---
Your prompt content for the agent...
```

### Step 4: Update System Prompt (if needed)

Edit `prompts/system.md` to add guidance about when and how to use the new tools.

## Rules

- **All tools inherit from `Tool`** — never create standalone functions
- **Always register** in `_build_default_registry()` — unregistered tools are invisible
- **Tool description is critical** — the LLM uses it to decide when to call the tool. Be precise.
- **Set `is_read_only = True`** for tools that only read data — enables parallel execution
- **Override `check_permissions()`** for tools that need fine-grained permission control
- **Return `ToolResult`** from `execute()` — set `is_error=True` for failures
- Use `structlog` logger — never `print()`
- Use `httpx` for HTTP requests (async), never `requests`

Now read the development document and build the agent tools.
