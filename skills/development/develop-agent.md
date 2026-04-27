---
description: Build AI agent using agent-template (port 8080), modeled after Claude Code architecture.
---
You are a senior AI engineer. You will receive a **development document** and build custom agent tools using [agent-template](https://github.com/madeinhash/agent-template).

## Template Conventions (from agent-template CLAUDE.md)

These are the rules of this codebase. Follow them exactly.

- **Language**: Python 3.11+, async-first, strict typing
- **LLM**: LiteLLM (unified interface — set `LLM_MODEL` in `.env`)
- **Port**: 8080
- **Architecture**: Agent Loop → Tool System → Permission System (modeled after Claude Code)
- **Tool base class**: `Tool` ABC in `src/tools/base.py` — ALL tools inherit from this
- **Tool registry**: `src/tools/registry.py` → `_build_default_registry()` — tools MUST be registered here
- **Config**: Pydantic Settings in `src/config.py` — never `os.environ`
- **Logging**: structlog `logger` — never `print()`
- **HTTP**: `httpx` (async) — never `requests`
- **Claude Code source**: [claudecode-source-code](https://github.com/madeinhash/claudecode-source-code) for architecture reference

Key Claude Code files to study:
- `src/Tool.ts` — tool type system (schema, permissions, execution)
- `src/tools/` — real tool implementations
- `src/QueryEngine.ts` — agent loop
- `src/hooks/toolPermission/` — permission pipeline

## Dev Doc → Code Mapping

When the development document defines an agent tool, map it directly:

| Dev Doc | Code File | What To Do |
|---------|-----------|------------|
| Tool `search_db` | `src/tools/builtin/search_db.py` | Inherit `Tool`, implement `name`, `description`, `parameters`, `execute()` |
| Tool `search_db` | `src/tools/registry.py` | Add `from src.tools.builtin.search_db import SearchDbTool` + `SearchDbTool()` to list |
| Skill `analyze` | `skills/analyze.md` | Markdown file with YAML frontmatter |
| System prompt change | `prompts/system.md` | Add tool usage guidance |

## Build Process

For EACH tool in the development document:

### 1. Create Tool
Create `src/tools/builtin/[name].py`:
- `name` — unique identifier
- `description` — the LLM reads this to decide when to call it. Be precise and specific.
- `parameters` — JSON Schema, sent to LLM as function schema
- `is_read_only` — set `True` if tool only reads data (enables parallel execution)
- `execute(args)` — implement tool logic, return `ToolResult(output=str, is_error=bool)`

### 2. Register Tool
In `src/tools/registry.py` → `_build_default_registry()`:
- Add import
- Add instance to the list

**Unregistered tools are invisible to the agent.**

### 3. Create Skills (if needed)
Create `skills/[name].md` with frontmatter.

### After EACH tool, verify:

```bash
pytest
```

If tests fail, fix before moving to the next tool. Do NOT skip this step.

## Rules

- Do NOT create standalone functions — always inherit from `Tool`
- Do NOT forget to register — unregistered = invisible
- Do NOT write vague tool descriptions — the LLM depends on them
- Do NOT use `requests` — use `httpx` (async)
- Do NOT use `print()` — use `structlog`
- Do NOT skip `pytest` after each tool

Now read the development document and build the agent.
