# Development Template Skills

AI-powered development skills for rapid product building. Give AI your idea, get a structured dev doc, then let AI build it using standardized templates.

## Workflow

```
1. User describes what they want to build
        ↓
2. /generate-dev-doc → AI produces a complete development document
        ↓
3. /develop-backend  → AI builds the API using backend-template
   /develop-frontend → AI builds the UI using frontend-template
   /develop-agent    → AI builds agent tools using agent-template
```

## Skills

| Skill | Description |
|-------|-------------|
| `generate-dev-doc` | Generate a complete development document from product requirements |
| `develop-frontend` | Build frontend pages/components from a dev doc |
| `develop-backend` | Build backend API endpoints from a dev doc |
| `develop-agent` | Build custom agent tools from a dev doc |

## Templates

| Template | Repo | Stack |
|----------|------|-------|
| Frontend | [frontend-template](https://github.com/madeinhash/frontend-template) | Next.js 15 + React 19 + Ant Design 6 + Tailwind CSS 4 |
| Backend | [backend-template](https://github.com/madeinhash/backend-template) | Express + TypeScript + Sequelize + PostgreSQL |
| Agent | [agent-template](https://github.com/madeinhash/agent-template) | Python + LiteLLM + Claude Code Architecture |

## Related Resources

- [UI UX Pro Max Skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) — AI-powered UI/UX design system for frontend development
- [Claude Code Source](https://github.com/madeinhash/claudecode-source-code) — Claude Code leaked source for agent architecture reference

## Document Template

See `templates/dev-doc.md` for the standard development document format.

## Usage

These skills are designed to be used with AI coding assistants (Claude Code, Cursor, etc.). Copy the skill content as a prompt, or integrate into your AI tool's skill/command system.
