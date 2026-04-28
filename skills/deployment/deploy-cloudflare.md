---
description: Deploy full stack (frontend + backend + database) to a single Cloudflare VPS. Simple and cheap for small projects.
---
You are a DevOps engineer. Deploy the entire stack to a single Cloudflare server. See [deployment-template](templates/deployment/) for full guides.

## Architecture

```
Cloudflare VPS (single server)
├── Nginx (reverse proxy, port 80/443)
│   ├── / → Frontend (Next.js, port 3000)
│   ├── /api/* → Backend (Express, port 4000)
│   └── /agent/* → Agent (Python, port 8080)
├── PostgreSQL (local, port 5432)
├── PM2 (process manager for Node.js)
└── systemd (for agent service)
```

## Setup Steps

### Step 1: Provision Server

Create a Cloudflare VPS (or any VPS) with Ubuntu 22.04+, minimum 1 vCPU, 2GB RAM.

### Step 2: Install Dependencies

```bash
# Node.js 22
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# Python 3.11
sudo apt-get install -y python3.11 python3.11-venv python3-pip

# PostgreSQL
sudo apt-get install -y postgresql postgresql-contrib
sudo -u postgres createuser --superuser $USER
createdb myproject

# Nginx
sudo apt-get install -y nginx

# PM2
sudo npm install -g pm2
```

### Step 3: Clone and Setup

```bash
# Backend
git clone YOUR_BACKEND_REPO ~/backend
cd ~/backend && npm install && npm run build
cp .env.template .env  # fill in DB credentials, JWT_SECRET, etc.
npm run db:migrate

# Frontend
git clone YOUR_FRONTEND_REPO ~/frontend
cd ~/frontend && npm install
cp .env.template .env.local  # set NEXT_PUBLIC_API_URL=https://yourdomain.com
npm run build

# Agent
git clone YOUR_AGENT_REPO ~/agent
cd ~/agent && python3.11 -m venv .venv && source .venv/bin/activate && pip install .
cp .env.template .env  # fill in API keys, PORT=8080
```

### Step 4: Configure Nginx

```nginx
# /etc/nginx/sites-available/myproject
server {
    listen 80;
    server_name yourdomain.com;

    # Frontend
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:4000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Agent
    location /agent/ {
        proxy_pass http://127.0.0.1:8080/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

### Step 5: Start Services

```bash
# Backend + Frontend via PM2
cd ~/backend && pm2 start npm --name backend -- run prod
cd ~/frontend && pm2 start npm --name frontend -- run start
pm2 save && pm2 startup

# Agent via systemd
sudo tee /etc/systemd/system/agent.service << EOF
[Unit]
Description=Agent Service
After=network.target

[Service]
WorkingDirectory=/root/agent
ExecStart=/root/agent/.venv/bin/python -m src.main
Restart=always
Environment=PORT=8080

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable agent && sudo systemctl start agent
```

### Step 6: HTTPS (optional)

```bash
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## Deploy Updates

```bash
# Backend
cd ~/backend && git pull && npm install && npm run build && npm run db:migrate && pm2 restart backend

# Frontend
cd ~/frontend && git pull && npm install && npm run build && pm2 restart frontend

# Agent
cd ~/agent && git pull && source .venv/bin/activate && pip install . && sudo systemctl restart agent
```

## Cost Estimate

| Resource | Monthly Cost |
|----------|-------------|
| Cloudflare VPS (1 vCPU, 2GB) | ~$5-10 |
| Domain (optional) | ~$1 |
| **Total** | **~$6-11/month** |
