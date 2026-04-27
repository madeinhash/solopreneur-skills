# Development Template Skills

AI-powered development skills for rapid product building. Give AI your idea, get a structured dev doc, then let AI build it using standardized templates.

## Workflow

```
1. User describes what they want to build
        ↓
2. /generate-dev-doc → AI produces a complete development document
        ↓
3. /develop-backend  → AI builds the API (security checks + testing)
   /develop-frontend → AI builds the UI (UI UX Pro Max design)
   /develop-agent    → AI builds agent tools (Claude Code architecture, port 8080)
        ↓
4. Deploy → see deployment-template
```

## Skills

| Skill | Description |
|-------|-------------|
| `generate-dev-doc` | Generate a complete development document from product requirements |
| `develop-frontend` | Build frontend from dev doc (requires UI UX Pro Max skill) |
| `develop-backend` | Build backend from dev doc (includes security checklist + testing) |
| `develop-agent` | Build agent tools from dev doc (Claude Code architecture) |
| `setup-permissions` | Recommended Claude Code permissions for development |

## Prerequisites

1. **Templates** — Clone the templates you need:
   - [frontend-template](https://github.com/madeinhash/frontend-template) — Next.js 15 + React 19 + Ant Design 6
   - [backend-template](https://github.com/madeinhash/backend-template) — Express + TypeScript + Sequelize + PostgreSQL
   - [agent-template](https://github.com/madeinhash/agent-template) — Python + LiteLLM (port 8080)

2. **UI/UX Skill** — Install [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) for frontend design decisions

3. **Permissions** — See `skills/setup-permissions.md` for recommended Claude Code permissions

4. **Deployment** — See [deployment-template](https://github.com/madeinhash/deployment-tempate) for AWS, Cloudflare, Vercel deployment guides

5. **Reference** — [Claude Code Source](https://github.com/madeinhash/claudecode-source-code) for agent architecture reference

## Template

See `templates/dev-doc.md` for the standard development document format (directly mappable to code).
