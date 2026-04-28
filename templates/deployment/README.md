# Deployment Template

Deployment skills and infrastructure templates for the full-stack template ecosystem.

## Deployment Options

| Platform | Best For | Cost | Auto-deploy |
|----------|----------|------|-------------|
| **AWS** | Backend + Agent (production) | ~$37/month | Yes (CodePipeline) |
| **Cloudflare VPS** | Full stack (small projects) | ~$6/month | Manual |
| **Vercel** | Frontend only | Free | Yes (push to main) |

## Architecture

```
AWS (backend + agent + database)
├── ECS Fargate: Backend (port 4000) + Agent (port 8080)
├── ALB: Path-based routing (/ → backend, /agent/* → agent)
├── RDS: PostgreSQL
└── CodePipeline: GitHub → CodeBuild → ECR → ECS

Cloudflare VPS (single server)
├── Nginx: Reverse proxy
├── PM2: Backend (4000) + Frontend (3000)
├── systemd: Agent (8080)
└── PostgreSQL: Local

Vercel (frontend only)
└── Next.js SSR + CDN + SSL
```

## Files

```
skills/
├── deploy-aws.md              # AWS deployment guide
├── deploy-cloudflare.md       # Cloudflare VPS deployment guide
└── deploy-vercel.md           # Vercel frontend deployment guide
templates/
└── aws-cloudformation.yaml    # Full AWS infrastructure as code
```

## Related Templates

- [frontend-template](https://github.com/madeinhash/frontend-template) — Next.js 15 + React 19
- [backend-template](https://github.com/madeinhash/backend-template) — Express + TypeScript + PostgreSQL
- [agent-template](https://github.com/madeinhash/agent-template) — Python + LiteLLM (port 8080)
- [solopreneur-skills](https://github.com/madeinhash/solopreneur-skills) — All product skills (development, deployment, business)
