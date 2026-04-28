---
description: Deploy the project. Guides you to the appropriate deployment method (AWS, Cloudflare, Vercel).
---
## Deployment

Choose a deployment method based on your needs. Detailed guides and templates are in the [deployment-template](templates/deployment/) repo.

| Platform | Best For | Cost | Guide |
|----------|----------|------|-------|
| **AWS** | Backend + Agent (production) | ~$37/month | `deployment-template/skills/deploy-aws.md` |
| **Cloudflare VPS** | Full stack on single server | ~$6/month | `deployment-template/skills/deploy-cloudflare.md` |
| **Vercel** | Frontend only | Free | `deployment-template/skills/deploy-vercel.md` |

### Recommended Setup

- **Frontend** → Vercel (free, auto-deploy, CDN)
- **Backend + Agent + Database** → AWS (ECS Fargate + RDS) or Cloudflare VPS

### AWS Infrastructure

The `deployment-template/templates/aws-cloudformation.yaml` provides a full CloudFormation template:
- ECS Fargate (backend port 4000 + agent port 8080)
- ALB with path-based routing (`/agent/*` → agent, `/*` → backend)
- RDS PostgreSQL
- CodePipeline CI/CD (GitHub → CodeBuild → ECR → ECS)
- Default VPC (no NAT Gateway, saves cost)

Go to the [deployment-template](templates/deployment/) repo for the full guides.
