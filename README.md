# Solopreneur Skills

All-in-one AI skills for building, deploying, and launching a product. From idea to revenue.

## Workflow

```
Idea → /generate-brd → Business Requirements Document
                ↓
     /generate-dev-doc → Development Document
                ↓
     /develop-backend  → Build API
     /develop-frontend → Build UI
     /develop-agent    → Build AI agent
                ↓
     /deploy           → Ship to production
                ↓
     /plan-launch      → Go to market
```

## Skills

### Business (`skills/business/`)

| Skill | Description | Template |
|-------|-------------|----------|
| `generate-brd` | Generate Business Requirements Document from product idea | [business-template](https://github.com/madeinhash/business-template) |
| `analyze-competitors` | Competitive landscape analysis | [business-template](https://github.com/madeinhash/business-template) |
| `plan-launch` | Launch plan with channels, timeline, first 100 users | [business-template](https://github.com/madeinhash/business-template) |

### Development (`skills/development/`)

| Skill | Description | Template |
|-------|-------------|----------|
| `generate-dev-doc` | Generate development document from BRD or requirements | — |
| `develop-frontend` | Build frontend from dev doc | [frontend-template](https://github.com/madeinhash/frontend-template) |
| `develop-backend` | Build backend from dev doc (security + testing) | [backend-template](https://github.com/madeinhash/backend-template) |
| `develop-agent` | Build AI agent from dev doc | [agent-template](https://github.com/madeinhash/agent-template) |
| `setup-permissions` | Claude Code permission config for development | — |

### Deployment (`skills/deployment/`)

| Skill | Description | Template |
|-------|-------------|----------|
| `deploy` | Deployment overview + guide to choose platform | [deployment-template](https://github.com/madeinhash/deployment-tempate) |
| `deploy-aws` | ECS Fargate + ALB + RDS + CodePipeline (~$37/month) | [deployment-template](https://github.com/madeinhash/deployment-tempate) |
| `deploy-cloudflare` | Single VPS full stack (~$6/month) | [deployment-template](https://github.com/madeinhash/deployment-tempate) |
| `deploy-vercel` | Frontend on Vercel (free) | [deployment-template](https://github.com/madeinhash/deployment-tempate) |

## All Repos

| Repo | What |
|------|------|
| [frontend-template](https://github.com/madeinhash/frontend-template) | Next.js 15 + React 19 + Ant Design 6 + Tailwind CSS 4 |
| [backend-template](https://github.com/madeinhash/backend-template) | Express + TypeScript + Sequelize + PostgreSQL |
| [agent-template](https://github.com/madeinhash/agent-template) | Python + LiteLLM + Claude Code architecture (port 8080) |
| [business-template](https://github.com/madeinhash/business-template) | BRD, pricing strategy, launch plan templates |
| [deployment-template](https://github.com/madeinhash/deployment-tempate) | AWS CloudFormation, Cloudflare VPS, Vercel guides |
| [claudecode-source-code](https://github.com/madeinhash/claudecode-source-code) | Claude Code source (agent architecture reference) |

## External Skills

| Skill | What |
|-------|------|
| [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | AI-powered UI/UX design (required for frontend development) |
