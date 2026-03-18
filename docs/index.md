# Jet — Project Documentation Index

**Project:** Jet v0.13.2 — Open-source, self-hosted project planning tool
**Generated:** 2026-03-18 | Scan Level: Exhaustive
**Repository:** github.com/makeplane/jet | License: AGPL-3.0

## Project Overview

- **Type:** Monorepo (Yarn Workspaces + Turbo) with 5 parts
- **Primary Languages:** TypeScript (frontend), Python (backend)
- **Architecture:** Next.js frontends + Django REST API + PostgreSQL + Redis + Celery

### Quick Reference

#### Web Dashboard (`web/`)
- **Type:** Next.js 12.3.2 / React 18 / TypeScript
- **State:** MobX (50+ stores)
- **Styling:** Tailwind CSS
- **Port:** 3000

#### Space — Public Sharing (`space/`)
- **Type:** Next.js 12.3.2 / React 18 / TypeScript
- **State:** MobX (4 stores)
- **Port:** 4000

#### API Server (`apiserver/`)
- **Type:** Django 4.2.5 / DRF 3.14.0 / Python 3.11
- **Database:** PostgreSQL 15.2
- **Tasks:** Celery 5.3.4
- **Port:** 8000

#### Shared Packages (`packages/`)
- **UI Library:** @jet/ui (React components)
- **Editors:** @jet/editor-core, rich-text-editor, lite-text-editor (TipTap)
- **Config:** Shared ESLint, Tailwind, TypeScript configs

#### Infrastructure (`deploy/`, `nginx/`)
- **Proxy:** Nginx 1.25.0
- **Containers:** Docker + Docker Compose
- **CI/CD:** GitHub Actions

## Generated Documentation

### Architecture
- [Project Overview](./project-overview.md)
- [Architecture — Web Dashboard](./architecture-web.md)
- [Architecture — API Server](./architecture-apiserver.md)
- [Architecture — Space (Public Sharing)](./architecture-space.md)
- [Architecture — Shared Packages](./architecture-packages.md)
- [Architecture — Infrastructure](./architecture-infra.md)
- [Integration Architecture](./integration-architecture.md)

### Technical Reference
- [Source Tree Analysis](./source-tree-analysis.md)
- [API Contracts — API Server](./api-contracts-apiserver.md)
- [Data Models — API Server](./data-models-apiserver.md)
- [Component Inventory — Web](./component-inventory-web.md)
- [Component Inventory — Packages](./component-inventory-packages.md)

### Development & Deployment
- [Development Guide](./development-guide.md)
- [Deployment Guide](./deployment-guide.md)

## Existing Documentation

- [README](../README.md) — Project overview, quick start, features, screenshots
- [Contributing Guide](../CONTRIBUTING.md) — Setup requirements, coding guidelines, PR process
- [Environment Setup](../ENV_SETUP.md) — Environment variable reference for all parts
- [Code of Conduct](../CODE_OF_CONDUCT.md) — Community code of conduct
- [License](../LICENSE.txt) — AGPL-3.0 license

## Getting Started

### For Development
1. Install prerequisites: Docker, Node.js 18+, Yarn
2. Run `./setup.sh` to generate environment files
3. Start services: `docker compose -f docker-compose-local.yml up -d`
4. Install deps: `yarn install`
5. Start dev: `yarn dev`
6. Open `http://localhost:3000`

### For Deployment
1. See [Deployment Guide](./deployment-guide.md) for Docker Compose self-hosting
2. Default credentials: `captain@jet.so` / `password123`

### For AI-Assisted Development
- Start with this `index.md` as context entry point
- Reference architecture docs for the part you're modifying
- Use [API Contracts](./api-contracts-apiserver.md) when working on frontend-backend integration
- Use [Data Models](./data-models-apiserver.md) when working on database changes
- Use [Component Inventory](./component-inventory-web.md) to find existing UI components
