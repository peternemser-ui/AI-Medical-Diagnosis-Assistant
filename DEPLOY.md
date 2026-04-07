# Deployment Guide

This guide covers deploying the AI Medical Diagnosis Assistant across several common platforms.

---

## Option 1: Docker Compose (Self-Hosted)

The project includes a full `docker-compose.yml` with PostgreSQL, Redis, backend, and frontend services.

```bash
# 1. Copy and configure environment variables
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys and secrets

# 2. Start all services
docker-compose up -d

# 3. Verify
curl http://localhost:8000/health
# Frontend available at http://localhost:3000
```

### Production variant

For production, target the nginx-based frontend image:

```bash
docker-compose -f docker-compose.yml up -d --build
```

The frontend Dockerfile has a `production` stage that builds static assets and serves them via nginx with API proxying to the backend.

---

## Option 2: Vercel + Railway (Split Deployment)

Best for teams that want managed infrastructure with zero ops.

### Frontend on Vercel

1. Push the repo to GitHub.
2. Import the project in [Vercel](https://vercel.com) and set the **Root Directory** to `frontend`.
3. Vercel auto-detects Vite. Build settings:
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
4. Edit `frontend/vercel.json` and replace `YOUR_BACKEND_URL` with your Railway backend URL (e.g., `https://meddiagnose-api.up.railway.app`).
5. Deploy.

### Backend on Railway

1. Create a new project in [Railway](https://railway.app).
2. Connect your repo and set the **Root Directory** to `backend`.
3. Railway reads the `Procfile` and `runtime.txt` automatically.
4. Add environment variables (see [Environment Variables](#environment-variables) below).
5. Provision a **PostgreSQL** plugin and a **Redis** plugin from the Railway dashboard. Railway auto-injects `DATABASE_URL` and `REDIS_URL`.
6. Deploy.

### Backend on Render (alternative)

1. Create a new **Web Service** on [Render](https://render.com).
2. Set the **Root Directory** to `backend`.
3. Render reads the `Procfile` and `runtime.txt`.
4. Add environment variables and provision managed PostgreSQL/Redis from the Render dashboard.
5. Deploy.

---

## Option 3: Fly.io (Full-Stack)

Fly.io can host the backend close to users globally. The included `fly.toml` targets the backend Dockerfile.

```bash
# 1. Install the Fly CLI
curl -L https://fly.io/install.sh | sh

# 2. Authenticate
fly auth login

# 3. Launch (first time — creates the app)
fly launch --config fly.toml

# 4. Set secrets (environment variables)
fly secrets set ANTHROPIC_API_KEY="sk-ant-..."
fly secrets set JWT_SECRET="your-jwt-secret"
fly secrets set ENCRYPTION_KEY="your-encryption-key"
fly secrets set DATABASE_URL="postgres://..."
fly secrets set REDIS_URL="redis://..."

# 5. Deploy
fly deploy

# 6. Verify
fly status
curl https://meddiagnose-ai.fly.dev/health
```

For the frontend, either deploy separately on Vercel/Netlify (recommended) or add a second Fly app using the frontend Dockerfile's `production` target.

---

## Option 4: Manual VPS (Ubuntu/Debian)

For full control on a VPS (DigitalOcean, Hetzner, AWS EC2, etc.).

### Prerequisites

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.12 python3.12-venv nginx certbot python3-certbot-nginx
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

### Backend setup

```bash
cd /opt
git clone https://github.com/YOUR_ORG/ai-medical-diagnosis-assistant.git app
cd app/backend

python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with production values

# Run with gunicorn for production
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend build

```bash
cd /opt/app/frontend
npm ci
npm run build
# Static files are in /opt/app/frontend/dist
```

### Nginx reverse proxy

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend static files
    root /opt/app/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Proxy API to backend
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 600s;
    }

    location /health {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
    }
}
```

```bash
# Enable HTTPS
sudo certbot --nginx -d your-domain.com
```

### Systemd service for the backend

```ini
# /etc/systemd/system/meddiagnose-api.service
[Unit]
Description=MedDiagnose AI Backend
After=network.target postgresql.service redis.service

[Service]
User=www-data
WorkingDirectory=/opt/app/backend
EnvironmentFile=/opt/app/backend/.env
ExecStart=/opt/app/backend/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now meddiagnose-api
```

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | Yes | Anthropic API key for Claude AI agents |
| `OPENAI_API_KEY` | No | Fallback for legacy GPT-4o mode |
| `JWT_SECRET` | Yes | Secret for signing authentication tokens |
| `ENCRYPTION_KEY` | Yes | Key for encrypting patient data at rest |
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `REDIS_URL` | Yes | Redis connection string |
| `CORS_ORIGINS` | No | Comma-separated allowed origins (defaults to localhost) |
| `FRONTEND_URL` | No | Frontend URL for email links and redirects |
| `OLLAMA_BASE_URL` | No | Local Ollama URL if using local models (default `http://localhost:11434`) |
| `AGENT_TIMEOUT` | No | Cloud agent timeout in seconds (default `180`) |
| `AGENT_TIMEOUT_HEAVY` | No | Timeout for specialist/treatment agents (default `240`) |
| `POSTGRES_PASSWORD` | Docker | PostgreSQL password for docker-compose |
| `REDIS_PASSWORD` | Docker | Redis password for docker-compose |

---

## Post-Deployment Checklist

- [ ] Set `CORS_ORIGINS` to include your production frontend URL
- [ ] Set `FRONTEND_URL` to your production frontend URL
- [ ] Generate strong random values for `JWT_SECRET` and `ENCRYPTION_KEY`
- [ ] Verify the `/health` endpoint returns a successful response
- [ ] Confirm agent pipeline works end-to-end via a test diagnosis
- [ ] Set up SSL/TLS (automatic on Vercel, Railway, Fly.io; manual with certbot on VPS)
- [ ] Configure rate limiting appropriate for your expected traffic
- [ ] Set up log aggregation and monitoring (e.g., Datadog, Sentry)
- [ ] Back up the PostgreSQL database on a schedule
