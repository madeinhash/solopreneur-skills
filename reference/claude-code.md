# Claude Code Source Reference

The agent template architecture is modeled after Anthropic's Claude Code CLI.

Full source code: **https://github.com/madeinhash/claudecode-source-code**

## Key Files to Study

| Claude Code File | Agent Template Equivalent | What It Does |
|-----------------|--------------------------|--------------|
| `src/QueryEngine.ts` | `templates/agent/src/engine/agent_loop.py` | Core agent loop |
| `src/Tool.ts` | `templates/agent/src/tools/base.py` | Base tool type system |
| `src/tools/` | `templates/agent/src/tools/builtin/` | Built-in tool implementations |
| `src/hooks/toolPermission/` | `templates/agent/src/permissions/checker.py` | Permission pipeline |
| `src/tools/AgentTool/` | `templates/agent/src/tools/builtin/agent_tool.py` | Sub-agent spawning |
| `src/skills/` | `templates/agent/skills/` | Skill/command system |
