# Agent Service — Python + LiteLLM + Claude Code Architecture

This template's architecture is modeled after Anthropic's Claude Code CLI. The full Claude Code source is available at **https://github.com/madeinhash/claudecode-source-code** — refer to it when adding new tools, extending the permission system, or building advanced features like multi-agent orchestration.

Key files to study in Claude Code source:
- `src/QueryEngine.ts` — core agent loop (our `engine/agent_loop.py`)
- `src/Tool.ts` — base tool type system (our `tools/base.py`)
- `src/tools/` — built-in tool implementations (our `tools/builtin/`)
- `src/hooks/toolPermission/` — permission pipeline (our `permissions/checker.py`)
- `src/tools/AgentTool/` — sub-agent spawning (our `tools/builtin/agent_tool.py`)
- `src/skills/` — skill/command system (our `skills/`)

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.template .env          # fill in LLM_MODEL and API keys
python -m src.main             # API server on port 8080
python -m src.main --cli       # interactive CLI
```

## Tech Stack

- **Language**: Python 3.11+ (strict typing, async-first)
- **LLM**: LiteLLM (unified interface — OpenAI, Anthropic, Azure, Bedrock, etc.)
- **API Server**: FastAPI + Uvicorn
- **Validation**: Pydantic v2
- **Logging**: structlog
- **CLI**: Rich (colored terminal)
- **Testing**: pytest + pytest-asyncio

## Project Structure

```
src/
├── main.py                         # Entry point (--cli for CLI mode)
├── server.py                       # FastAPI app (/api/chat, /api/tools, /api/skills)
├── cli.py                          # Interactive CLI with permission prompts
├── config.py                       # Pydantic Settings (reads .env)
├── logger.py                       # structlog setup
├── types.py                        # Core types (Message, ToolCall, PermissionRule, ToolResult)
├── schemas.py                      # API request/response models
├── engine/
│   ├── llm.py                      # LiteLLM wrapper
│   └── agent_loop.py               # Core loop: LLM → tool calls → permission → execute → repeat
├── tools/
│   ├── base.py                     # Base Tool ABC (all tools inherit this)
│   ├── registry.py                 # ToolRegistry — tool registration and lookup
│   └── builtin/                    # 9 built-in tools
│       ├── bash.py                 # Shell commands (with command safety classification)
│       ├── read_file.py            # Read files with line numbers
│       ├── write_file.py           # Create/overwrite files
│       ├── edit_file.py            # Find-and-replace editing
│       ├── glob_tool.py            # File pattern matching
│       ├── grep_tool.py            # Content search (regex)
│       ├── web_fetch.py            # Fetch URL content
│       ├── agent_tool.py           # Spawn sub-agent for sub-tasks
│       └── ask_user.py             # Ask user for clarification
├── permissions/
│   └── checker.py                  # Rule-based allow/deny/ask permission pipeline
└── skills/
    └── loader.py                   # Load markdown skill files with YAML frontmatter
skills/                             # Skill definitions (markdown files)
prompts/
└── system.md                       # Agent system prompt
tests/
```

## Architecture: Agent Loop → Tool System → Permission System

**Agent Loop** (`engine/agent_loop.py`): LLM call → parse tool_calls → check permissions → execute → append results → loop until done or max iterations.

- Read-only tools (`is_read_only=True`) run **in parallel**. Write tools run **serially**.
- Each iteration: one LLM call, then all tool calls from that response.

**Tool System** (`tools/base.py`): Every tool is a class inheriting `Tool` ABC with:
- `name`, `description`, `parameters` (JSON Schema) — sent to LLM as function schema
- `is_read_only` / `is_destructive` — safety flags for concurrency and permissions
- `validate_input(args)` → return error string or None
- `check_permissions(args)` → return `PermissionResult(behavior=ALLOW|DENY|ASK)`
- `execute(args)` → return `ToolResult(output=str, is_error=bool)`

**Permission System** (`permissions/checker.py`): Multi-stage pipeline:
1. `tool.validate_input()` — reject bad input
2. `tool.check_permissions()` — tool-specific rules (e.g. bash safe-command list)
3. Deny rules — block destructive patterns (`rm -rf`, etc.)
4. Allow rules — permit known-safe patterns
5. Mode fallback — `ask` (prompt user) | `auto` (allow all) | `strict` (deny unless explicit)

**Skill System** (`skills/`): Markdown files with YAML frontmatter. Loaded at runtime. Invoked via `/skill-name` in CLI.

**Sub-Agent** (`tools/builtin/agent_tool.py`): Main agent spawns child `AgentLoop` with isolated messages and reduced iteration limit.

## Scripts

| Command | Description |
|---------|-------------|
| `python -m src.main` | API server (auto-reload in dev) |
| `python -m src.main --cli` | Interactive CLI |
| `pytest` | Run tests |
| `ruff check src/` | Lint |
| `ruff format src/` | Format |
| `mypy src/` | Type-check |

## Adding a New Tool (IMPORTANT)

1. Create file in `src/tools/builtin/` — inherit from `Tool`
2. Implement all required properties and `execute()`:

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
        return "What this tool does — the LLM reads this to decide when to call it."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "param1": {"type": "string", "description": "What param1 is"},
            },
            "required": ["param1"],
        }

    @property
    def is_read_only(self) -> bool:
        return False  # set True if tool only reads data

    async def execute(self, args: dict[str, Any]) -> ToolResult:
        # implement tool logic here
        return ToolResult(output="result string")
```

3. **Register the tool** in `src/tools/registry.py` → `_build_default_registry()`:
   - Add import: `from src.tools.builtin.my_tool import MyTool`
   - Add to the list: `MyTool()`

Without step 3, the agent will NOT see the tool.

## Adding a New Skill

Create a `.md` file in `skills/` directory:

```markdown
---
description: One-line description of what this skill does
allowed_tools: [read_file, bash, grep]
---
Your prompt content here. This becomes the user message sent to the agent.
```

- `description` — shown in `/api/skills` and CLI help
- `allowed_tools` — optional, not enforced yet (for future use)
- Invoke in CLI: `/skill-name optional-extra-context`

## Coding Conventions

- All source in `src/`, async-first (`async def` everywhere)
- Type hints on all function signatures
- All tools inherit from `Tool` base class — never create standalone tool functions
- All config via `src/config.py` — never read `os.environ` directly
- Use `structlog` `logger` — never `print()` in production code (CLI `console.print` is OK)
- Use Pydantic models for API schemas
- Import `ToolResult` from `src.types` for tool return values
- Import `Tool` from `src.tools.base` for tool base class

## API Endpoints

- `GET /health` — health check
- `GET /api/tools` — list all registered tools
- `GET /api/skills` — list all loaded skills
- `POST /api/chat` — send message to agent
  - Body: `{ "message": "...", "session_id": "optional" }`
  - Response: `{ "response": "...", "session_id": "...", "tool_calls_count": 0 }`

## Environment Variables

See `.env.template`. Key ones:
- `LLM_MODEL` — LiteLLM model string (`gpt-4o`, `claude-sonnet-4-20250514`, `azure/gpt-4o`)
- `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` — LLM provider keys
- `PERMISSION_MODE` — `ask` | `auto` | `strict`
- `AGENT_MAX_ITERATIONS` — max tool-calling loops per request (default 25)
- `AGENT_SYSTEM_PROMPT_FILE` — path to system prompt (default `prompts/system.md`)
