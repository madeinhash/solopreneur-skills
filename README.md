# Solopreneur Skills

All-in-one AI toolkit for solopreneurs. From idea to revenue — business planning, development, deployment, all in one repo.

Clone this repo, point AI at it, build your product.

## Workflow

```
Idea → /generate-brd        → Business Requirements Document
            ↓
       /generate-dev-doc     → Development Document
            ↓
       /develop-backend      → Build API
       /develop-frontend     → Build UI
       /develop-agent        → Build AI agent
            ↓
       /deploy               → Ship to production
            ↓
       /plan-launch          → Go to market
```

## Skills

### Business (`skills/business/`)

| Skill | Description |
|-------|-------------|
| `generate-brd` | Generate Business Requirements Document from product idea |
| `analyze-competitors` | Competitive landscape analysis |
| `plan-launch` | Launch plan — channels, timeline, first 100 users |

### Development (`skills/development/`)

| Skill | Description |
|-------|-------------|
| `generate-dev-doc` | Generate development document from BRD or requirements |
| `develop-frontend` | Build frontend from dev doc (+ UI UX Pro Max for design) |
| `develop-backend` | Build backend from dev doc (security checklist + testing) |
| `develop-agent` | Build AI agent from dev doc (Claude Code architecture) |
| `setup-permissions` | Claude Code permission config |

### Deployment (`skills/deployment/`)

| Skill | Description |
|-------|-------------|
| `deploy` | Choose deployment platform |
| `deploy-aws` | ECS Fargate + ALB + RDS + CodePipeline (~$37/month) |
| `deploy-cloudflare` | Single VPS full stack (~$6/month) |
| `deploy-vercel` | Frontend on Vercel (free) |

## Templates

All templates are included in this repo — no separate repos needed.

```
templates/
├── frontend/       # Next.js 15 + React 19 + Ant Design 6 + Tailwind CSS 4
├── backend/        # Express + TypeScript + Sequelize + PostgreSQL
├── agent/          # Python + LiteLLM + Claude Code architecture (port 8080)
├── business/       # BRD, pricing strategy, launch plan document templates
└── deployment/     # AWS CloudFormation, Cloudflare VPS, Vercel guides
reference/
└── claude-code.md  # Claude Code source reference for agent architecture
```

## Quick Start

```bash
git clone https://github.com/madeinhash/solopreneur-skills.git
cd solopreneur-skills

# Start a new project — copy the template you need
cp -r templates/frontend ../my-project-frontend
cp -r templates/backend ../my-project-backend
cp -r templates/agent ../my-project-agent    # if needed
```

## External Dependencies

| What | Link | Required For |
|------|------|-------------|
| UI UX Pro Max | [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Frontend design decisions |
| Claude Code Source | [claudecode-source-code](https://github.com/madeinhash/claudecode-source-code) | Agent architecture reference |
