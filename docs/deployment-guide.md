# Deployment Guide

**Generated:** 2026-03-18

## Deployment Options

| Method | Complexity | Best For |
|--------|-----------|----------|
| Docker Compose (Self-hosted) | Low | Small teams, single server |
| Docker Hub Images | Medium | Custom infrastructure |
| Heroku | Low | Quick start, managed hosting |
| Custom Kubernetes | High | Large scale, enterprise |

## Self-Hosted Deployment (Docker Compose)

### Quick Start

```bash
# 1. Download deployment files
mkdir plane && cd plane
curl -fsSL https://raw.githubusercontent.com/makeplane/plane/master/deploy/selfhost/install.sh -o install.sh
chmod +x install.sh

# 2. Run installer
./install.sh
# Choose: 1 (Install)
```

### Manual Setup

```bash
# 1. Clone repository
git clone https://github.com/makeplane/plane.git
cd plane/deploy/selfhost

# 2. Configure environment
cp variables.env .env
# Edit .env with your values (see Environment Variables below)

# 3. Start services
docker compose up -d
```

### Services Deployed

| Service | Image | Port | Resources |
|---------|-------|------|-----------|
| web | makeplane/plane-frontend | 3000 | Next.js SSR |
| space | makeplane/plane-space | 3000 | Next.js SSR |
| api | makeplane/plane-backend | 8000 | Django/Gunicorn |
| worker | makeplane/plane-backend | - | Celery worker |
| beat-worker | makeplane/plane-backend | - | Celery Beat |
| plane-db | postgres:15.2-alpine | 5432 | PostgreSQL |
| plane-redis | redis:6.2.7-alpine | 6379 | Redis |
| plane-minio | minio/minio | 9000 | S3 storage |
| proxy | makeplane/plane-proxy | 80 | Nginx |

### Persistent Volumes

| Volume | Service | Purpose |
|--------|---------|---------|
| pgdata | plane-db | Database storage |
| redisdata | plane-redis | Redis persistence |
| uploads | plane-minio | File uploads |

## Environment Variables

### Required

| Variable | Default | Description |
|----------|---------|-------------|
| SECRET_KEY | Auto-generated | Django secret key |
| DATABASE_URL | postgresql://... | PostgreSQL connection |
| REDIS_URL | redis://... | Redis connection |
| WEB_URL | http://localhost | Public URL |
| NGINX_PORT | 80 | Nginx listen port |

### Database

| Variable | Default | Description |
|----------|---------|-------------|
| PGUSER | plane | Database user |
| PGPASSWORD | plane | Database password |
| PGHOST | plane-db | Database host |
| PGDATABASE | plane | Database name |

### Storage (MinIO/S3)

| Variable | Default | Description |
|----------|---------|-------------|
| AWS_ACCESS_KEY_ID | access-key | S3 access key |
| AWS_SECRET_ACCESS_KEY | secret-key | S3 secret key |
| AWS_S3_ENDPOINT_URL | http://plane-minio:9000 | S3 endpoint |
| AWS_S3_BUCKET_NAME | uploads | Bucket name |
| FILE_SIZE_LIMIT | 5242880 | Max upload size (bytes) |
| USE_MINIO | 1 | Use MinIO (0 for AWS S3) |

### Email (SMTP)

| Variable | Default | Description |
|----------|---------|-------------|
| EMAIL_HOST | - | SMTP server |
| EMAIL_HOST_USER | - | SMTP username |
| EMAIL_HOST_PASSWORD | - | SMTP password |
| EMAIL_PORT | 587 | SMTP port |
| EMAIL_FROM | Team Plane <team@mailer.plane.so> | Sender address |
| EMAIL_USE_TLS | 1 | Use TLS |

### Optional Integrations

| Variable | Default | Description |
|----------|---------|-------------|
| OPENAI_API_KEY | - | OpenAI API key (AI features) |
| GPT_ENGINE | gpt-3.5-turbo | GPT model |
| GITHUB_CLIENT_SECRET | - | GitHub OAuth/sync |
| SENTRY_DSN | - | Sentry error tracking |
| ENABLE_SIGNUP | 1 | Allow new registrations |

### Default Credentials

| Variable | Default | Description |
|----------|---------|-------------|
| DEFAULT_EMAIL | captain@plane.so | Admin email |
| DEFAULT_PASSWORD | password123 | Admin password |

## Nginx Proxy Configuration

Nginx routes traffic to internal services:

```
/          → web:3000     (Main dashboard)
/api/      → api:8000     (REST API)
/spaces/   → space:3000   (Public sharing)
/uploads/  → minio:9000   (File storage)
```

**Security Headers:** HSTS, X-Content-Type-Options, Referrer-Policy, Permissions-Policy

**SSL/TLS:** Not included by default. Use a reverse proxy (Caddy, Traefik) or load balancer in front of Nginx for HTTPS.

## Heroku Deployment

```bash
# Using Heroku CLI
heroku create my-plane-app
heroku stack:set container
git push heroku main
```

**Addons:** PostgreSQL (mini), Redis (mini)
**Buildpacks:** Python, Node.js
**Procfile:** Defines web, worker, beat processes

## Docker Hub Images

Published on GitHub releases:

| Image | Tag Pattern | Description |
|-------|-------------|-------------|
| `makeplane/plane-frontend` | `v0.13.2`, `latest` | Web dashboard |
| `makeplane/plane-backend` | `v0.13.2`, `latest` | API + Worker |
| `makeplane/plane-space` | `v0.13.2`, `latest` | Public sharing |
| `makeplane/plane-proxy` | `v0.13.2`, `latest` | Nginx proxy |

## Operations

### Database Backup
```bash
docker compose exec plane-db pg_dump -U plane plane > backup.sql
```

### Database Restore
```bash
docker compose exec -T plane-db psql -U plane plane < backup.sql
```

### Run Migrations
```bash
docker compose exec api python manage.py migrate
```

### Create Superuser
```bash
docker compose exec api python manage.py createsuperuser
```

### View Logs
```bash
docker compose logs -f api        # API server logs
docker compose logs -f worker     # Celery worker logs
docker compose logs -f proxy      # Nginx access logs
```

### Upgrade
```bash
# Pull latest images
docker compose pull

# Restart services
docker compose up -d

# Run migrations
docker compose exec api python manage.py migrate
```

## CI/CD Pipeline

GitHub Actions automatically builds and publishes Docker images on release:

1. PR → `build-test-pull-request.yml` validates build
2. Merge to master → optional CE→EE sync
3. GitHub Release → `update-docker-images.yml` pushes to Docker Hub

## Production Considerations

- **SSL/TLS:** Add reverse proxy (Caddy, Traefik, AWS ALB) for HTTPS
- **Database:** Use managed PostgreSQL (RDS, Cloud SQL) for production
- **Redis:** Use managed Redis (ElastiCache, Memorystore) for production
- **Storage:** Switch `USE_MINIO=0` and configure AWS S3 directly
- **Email:** Configure real SMTP (SendGrid, SES, Mailgun)
- **Monitoring:** Enable Sentry (`SENTRY_DSN`), configure log aggregation
- **Backups:** Automated database backups, S3 versioning
- **Scaling:** Separate API and worker containers, horizontal scaling behind load balancer
