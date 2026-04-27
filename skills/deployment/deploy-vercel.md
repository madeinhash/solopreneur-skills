---
description: Deploy frontend to Vercel. Recommended for frontend-only deployment — backend and agent deploy separately on AWS or Cloudflare.
---
You are a DevOps engineer. Deploy the frontend to Vercel. See [deployment-template](https://github.com/madeinhash/deployment-tempate) for full guides.

## Architecture

```
Vercel (frontend only)
└── Next.js 15 (SSR + static)
    └── Calls backend API at NEXT_PUBLIC_API_URL
```

Vercel handles: build, CDN, SSL, preview deployments, custom domains.

## Setup Steps

### Step 1: Connect GitHub

```bash
# Install Vercel CLI
npm i -g vercel

# Link project
cd frontend
vercel link
```

Or connect via Vercel dashboard: Import Project → Select GitHub repo.

### Step 2: Set Environment Variables

In Vercel dashboard → Project → Settings → Environment Variables:

| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_API_URL` | `https://your-backend-domain.com` (ALB endpoint or Cloudflare domain) |

### Step 3: Deploy

```bash
# Deploy to production
vercel --prod
```

Or just push to `main` — Vercel auto-deploys.

### Step 4: Custom Domain (optional)

In Vercel dashboard → Project → Settings → Domains → Add your domain.

## Notes

- Every push to `main` triggers a production deploy
- Every PR gets a preview deployment URL
- Make sure backend `CORS_WHITELIST` includes your Vercel domain
- Vercel free tier: 100GB bandwidth, unlimited deploys

## Cost

| Plan | Monthly Cost |
|------|-------------|
| Hobby (personal) | Free |
| Pro (team) | $20/user |
