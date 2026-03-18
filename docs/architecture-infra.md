# Architecture - Infrastructure

**Generated:** 2026-03-18
**Part:** infra
**Type:** Docker / Nginx / CI/CD

## Overview

Infrastructure configuration for deploying Plane as a containerized application with Nginx reverse proxy, Docker Compose orchestration, and GitHub Actions CI/CD.

## Docker Architecture

### Production Dockerfile (Root)

Multi-stage build with 3 stages:

**Stage 1: Builder** (node:18-alpine)
- Turbo monorepo pruning for web and space apps
- Prunes unnecessary packages

**Stage 2: Installer** (node:18-alpine)
- Installs dependencies from pruned lockfile
- Builds all apps with `turbo run build`
- Next.js standalone output mode
- Environment variable substitution script

**Stage 3: Backend** (python:3.11.1-alpine3.17)
- Installs Python dependencies
- Copies built frontend artifacts from Stage 2
- Installs nginx + supervisor for process management
- Runs as non-root user (`captain` in `plane` group)
- Exposes port 80
- Supervisor manages: nginx, web (Node), space (Node)

### Development Dockerfiles

- `apiserver/Dockerfile.dev` — Python dev server with hot reload
- `apiserver/Dockerfile.api` — Production API server (Gunicorn)

## Docker Compose Configurations

### docker-compose.yml (Full Development)

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| web | Mounted source | 3000 | Next.js dev server |
| space | Mounted source | 4000 | Next.js dev server |
| api | Custom Dockerfile.dev | 8000 | Django dev server |
| worker | Same as api | - | Celery worker |
| beat-worker | Same as api | - | Celery Beat scheduler |
| plane-db | postgres:15.2-alpine | 5432 | PostgreSQL |
| plane-redis | redis:6.2.7-alpine | 6379 | Redis |
| plane-minio | minio/minio | 9000 | S3-compatible storage |
| proxy | nginx (custom) | 80 | Reverse proxy |

Network: `dev_env` (bridge)

### docker-compose-local.yml (Local Dev)

Lightweight — only external services:
| Service | Port | Purpose |
|---------|------|---------|
| plane-db | 5432 | PostgreSQL |
| plane-redis | 6379 | Redis |
| plane-minio | 9000 | MinIO |
| createbuckets | - | Auto-create S3 bucket |

For developers running Next.js and Django locally (not in containers).

### deploy/selfhost/docker-compose.yml (Self-Hosted Production)

Full production deployment with:
- All services containerized
- Shared env via `x-app-env` YAML anchor
- PostgreSQL with `max_connections=1000`
- Named volumes for persistence
- Health checks
- Restart policies

## Nginx Configuration

### nginx.conf.template

```nginx
server {
    listen 80;

    # Main web app
    location / {
        proxy_pass http://web:3000/;
    }

    # REST API
    location /api/ {
        proxy_pass http://api:8000/api/;
    }

    # Public sharing app
    location /spaces/ {
        proxy_pass http://space:3000/;
    }

    # File uploads (MinIO/S3)
    location /${BUCKET_NAME}/ {
        proxy_pass http://plane-minio:9000/uploads/;
    }
}
```

**Security Headers:**
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: no-referrer-when-downgrade`
- `Permissions-Policy: interest-cohort=()`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`

**Client Max Body Size:** Configurable via `FILE_SIZE_LIMIT` (default 5MB)

### nginx-single-docker-image.conf

Simplified config for the all-in-one Docker image (production Dockerfile) — routes to localhost services.

### supervisor.conf

Process management for the single Docker image:
- nginx (foreground)
- Node.js web server
- Node.js space server

## CI/CD Pipelines (GitHub Actions)

### build-test-pull-request.yml

**Trigger:** Pull requests (opened, synchronize)

```yaml
Steps:
1. Checkout code
2. Setup Node.js 18.x with yarn cache
3. Detect changed files (uses tj-actions/changed-files)
4. Conditional builds:
   - Build web/ if web/** changed
   - Build space/ if space/** changed
```

### create-sync-pr.yml

**Trigger:** PR merged to master
**Purpose:** Sync community edition changes to enterprise edition repository

```yaml
Steps:
1. Verify source repo is makeplane/plane
2. Checkout code
3. Push branch to target (EE) repo
4. Create PR with [SYNC] prefix
```

### update-docker-images.yml

**Trigger:** GitHub releases (released, prereleased)
**Purpose:** Build and push 4 Docker images to Docker Hub

| Image | Source | Description |
|-------|--------|-------------|
| plane-frontend | web/ | Main dashboard |
| plane-backend | apiserver/ | API server |
| plane-space | space/ | Public sharing |
| plane-proxy | nginx/ | Reverse proxy |

```yaml
Steps per image:
1. Checkout code
2. Setup Docker Buildx
3. Login to Docker Hub
4. Extract metadata (tags from release version)
5. Build and push
```

## Self-Hosted Deployment

### install.sh (Interactive Installer)

Menu-driven script for self-hosting:
- `install` — Full installation from scratch
- `download` — Download latest Docker Compose config
- `startServices` — Start all services
- `stopServices` — Stop all services
- `restartServices` — Restart services
- `upgrade` — Upgrade to latest version

Maintains archive of previous configurations.

### variables.env (Template)

63 environment variables across categories:
- App settings (SECRET_KEY, WEB_URL, DEBUG)
- Database (PG*)
- Redis
- Email (SMTP)
- Storage (AWS/MinIO)
- OAuth (Google, GitHub)
- OpenAI
- Sentry

## Heroku Deployment

- **app.json** — Heroku manifest with PostgreSQL mini, Redis mini addons
- **heroku.yml** — Docker deployment via `deploy/heroku/Dockerfile`
- **Buildpacks:** Python + Node.js

## Setup Scripts

### setup.sh
```bash
# Generates .env files from .env.example templates
# Auto-generates Django SECRET_KEY using /dev/urandom
# Creates web/.env, space/.env, apiserver/.env
```

### start.sh
```bash
# Simple Node.js process starter
# Usage: start.sh <path-to-server.js>
node $1
```
