---
description: Deploy backend + agent to AWS using ECS Fargate + ALB + RDS PostgreSQL + CodePipeline CI/CD. Uses default VPC (no NAT Gateway) to save cost.
---
You are a DevOps engineer. Deploy the project to AWS using the CloudFormation template from [deployment-template](templates/deployment/).

## Architecture

```
Internet → ALB (port 80/443)
             ├── /* → Backend (ECS Fargate, port 4000)
             └── /agent/* → Agent (ECS Fargate, port 8080)

RDS PostgreSQL ← Backend
CodePipeline (GitHub → CodeBuild → ECR → ECS Deploy) × 2 pipelines
```

- **Default VPC** — no private subnets, no NAT Gateway (saves ~$30/month)
- **ECS Fargate** — serverless containers, no EC2 to manage
- **ALB** — path-based routing: `/agent/*` goes to agent service, everything else to backend
- **RDS PostgreSQL** — managed database, `db.t4g.micro` for free tier
- **CodePipeline** — push to GitHub `main` → auto build + deploy

## Prerequisites

1. **AWS CLI** configured with credentials
2. **GitHub CodeStar Connection** — create in AWS Console → Developer Tools → Connections → Create connection → GitHub. Copy the ARN.
3. **Backend Dockerfile** — already exists in backend-template (port 4000)
4. **Agent Dockerfile** — already exists in agent-template (port 8080)

## Deploy Steps

### Step 1: Export Default VPC info

The CloudFormation template needs default VPC subnets. Create a helper stack or export manually:

```bash
# Get default VPC ID
aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query "Vpcs[0].VpcId" --output text

# Get default subnets (need at least 2 for ALB)
aws ec2 describe-subnets --filters "Name=vpc-id,Values=<VPC_ID>" --query "Subnets[*].SubnetId" --output text
```

### Step 2: Deploy CloudFormation

Use the template at `templates/aws-cloudformation.yaml`:

```bash
aws cloudformation deploy \
  --template-file templates/aws-cloudformation.yaml \
  --stack-name myproject-prod \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    ProjectName=myproject \
    Environment=production \
    GitHubOwner=YOUR_GITHUB_USERNAME \
    BackendRepo=YOUR_BACKEND_REPO \
    AgentRepo=YOUR_AGENT_REPO \
    GitHubBranch=main \
    GitHubConnectionArn=arn:aws:codestar-connections:REGION:ACCOUNT:connection/CONNECTION_ID \
    DBUsername=postgres \
    DBPassword=YOUR_SECURE_PASSWORD \
    JWTSecret=YOUR_JWT_SECRET \
    OpenAIApiKey=sk-xxx \
    LLMModel=gpt-4o
```

### Step 3: Push initial Docker images

The first deploy needs images in ECR before ECS can start:

```bash
# Login to ECR
aws ecr get-login-password --region REGION | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com

# Backend
cd backend
docker build -t myproject-backend .
docker tag myproject-backend:latest ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/myproject-backend:latest
docker push ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/myproject-backend:latest

# Agent
cd ../agent
docker build -t myproject-agent .
docker tag myproject-agent:latest ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/myproject-agent:latest
docker push ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/myproject-agent:latest
```

### Step 4: Run database migrations

```bash
# Connect to RDS and run migrations (use the RDS endpoint from CloudFormation outputs)
DB_HOST=xxx.rds.amazonaws.com DB_USER=postgres DB_PASSWORD=xxx DB_TABLE=myproject npm run db:migrate
```

### Step 5: Verify

```bash
# Get ALB endpoint
aws cloudformation describe-stacks --stack-name myproject-prod --query "Stacks[0].Outputs"

# Test
curl http://ALB_ENDPOINT/health
curl http://ALB_ENDPOINT/agent/health
```

After this, every push to `main` auto-deploys via CodePipeline.

## Cost Estimate (minimal)

| Resource | Monthly Cost |
|----------|-------------|
| ECS Fargate (2 × 0.25 vCPU, 0.5GB) | ~$18 |
| ALB | ~$16 |
| RDS db.t4g.micro (free tier 1yr) | $0 → ~$13 |
| ECR | ~$1 |
| CodePipeline | ~$2 |
| **Total** | **~$37/month** (with free tier) |

## Notes

- Frontend deploys to Vercel separately (see `deploy-vercel` skill)
- Set `CORS_WHITELIST` in backend env to your Vercel domain
- For HTTPS, add an ACM certificate and update ALB listener to port 443
- For custom domain, add Route 53 alias record pointing to ALB
