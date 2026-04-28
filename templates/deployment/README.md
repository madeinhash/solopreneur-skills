# Deployment Templates

Infrastructure templates and deployment guides.

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
templates/
└── aws-cloudformation.yaml    # Full AWS infrastructure as code
```

Deployment skills are in `skills/deployment/`.
