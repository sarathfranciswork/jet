# Plane - Project Overview

**Project:** Plane
**Version:** 0.13.2
**License:** AGPL-3.0
**Repository:** github.com/makeplane/plane
**Generated:** 2026-03-18

## Executive Summary

Plane is an open-source, self-hosted project planning and management tool designed for software development teams. It provides issue tracking, sprint planning (Cycles), feature grouping (Modules), custom views, wiki-like pages, and analytics — all with a modern, responsive web interface.

The platform supports multi-tenant workspaces with role-based access control, real-time collaboration, and integrations with GitHub, Slack, and OpenAI for AI-powered features.

## Technology Stack Summary

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend (Web) | Next.js / React / TypeScript | 12.3.2 / 18.2.0 / 4.7.4 |
| Frontend (Space) | Next.js / React / TypeScript | 12.3.2 / 18.2.0 / 4.7.4 |
| State Management | MobX | 6.10.0 |
| Styling | Tailwind CSS | 3.3.3 |
| UI Components | @plane/ui, Blueprint.js, Headless UI, MUI | Custom |
| Rich Text Editor | TipTap (ProseMirror) | 2.1.x |
| Backend API | Django / Django REST Framework | 4.2.5 / 3.14.0 |
| Background Tasks | Celery + Celery Beat | 5.3.4 |
| Database | PostgreSQL | 15.2 |
| Cache / Message Broker | Redis | 6.2.7 |
| File Storage | MinIO (S3-compatible) | Latest |
| Reverse Proxy | Nginx | 1.25.0 |
| Containerization | Docker + Docker Compose | Latest |
| Monorepo Tooling | Turbo + Yarn Workspaces | 1.10.16 |
| CI/CD | GitHub Actions | - |

## Architecture Type

**Monorepo** with 5 distinct parts:

| Part | Type | Path | Purpose |
|------|------|------|---------|
| Web | Next.js Frontend | `web/` | Main project management dashboard |
| Space | Next.js Frontend | `space/` | Public project sharing / read-only views |
| API Server | Django Backend | `apiserver/` | REST API, business logic, background tasks |
| Packages | TypeScript Libraries | `packages/` | Shared UI components, editors, configs |
| Infrastructure | Docker / Nginx | `deploy/`, `nginx/`, root configs | Deployment, reverse proxy, CI/CD |

## Repository Structure

```
jet/ (plane)
├── web/                # Main Next.js dashboard app (port 3000)
├── space/              # Public sharing Next.js app (port 4000)
├── apiserver/          # Django REST API backend (port 8000)
├── packages/           # Shared TypeScript packages
│   ├── ui/             # @plane/ui component library
│   ├── editor/         # TipTap-based editor packages
│   │   ├── core/       # @plane/editor-core
│   │   ├── rich-text-editor/  # @plane/rich-text-editor
│   │   └── lite-text-editor/  # @plane/lite-text-editor
│   ├── eslint-config-custom/
│   ├── tailwind-config-custom/
│   └── tsconfig/
├── deploy/             # Deployment configurations
├── nginx/              # Nginx reverse proxy
├── docker-compose.yml  # Development Docker setup
├── Dockerfile          # Production multi-stage build
├── turbo.json          # Turbo monorepo config
├── package.json        # Root workspace config
└── setup.sh            # Development setup script
```

## Key Features

- **Issue Planning & Tracking** — Rich text descriptions, sub-issues, labels, priorities, assignees, dates
- **Multiple Layouts** — List, Kanban, Calendar, Spreadsheet, Gantt chart views
- **Cycles (Sprints)** — Time-boxed iterations with issue grouping and progress tracking
- **Modules** — Feature-based issue grouping across cycles
- **Custom Views** — Saved filter configurations for personalized issue lists
- **Pages** — Wiki-like documentation with issue embedding
- **Inbox** — Triage incoming issues before adding to project
- **Analytics** — Custom analytics with charts and export
- **Command Palette** — Keyboard-driven navigation and actions (Cmd+K)
- **GitHub Sync** — Two-way issue synchronization
- **Slack Integration** — Channel notifications
- **AI Features** — OpenAI-powered issue assistance
- **Public Sharing** — Publish projects for external read-only access
- **Self-Hosted** — Complete Docker Compose deployment

## Links to Detailed Documentation

- [Architecture - Web](./architecture-web.md)
- [Architecture - API Server](./architecture-apiserver.md)
- [Architecture - Space](./architecture-space.md)
- [Architecture - Packages](./architecture-packages.md)
- [Architecture - Infrastructure](./architecture-infra.md)
- [Source Tree Analysis](./source-tree-analysis.md)
- [API Contracts](./api-contracts-apiserver.md)
- [Data Models](./data-models-apiserver.md)
- [Component Inventory - Web](./component-inventory-web.md)
- [Component Inventory - Packages](./component-inventory-packages.md)
- [Development Guide](./development-guide.md)
- [Deployment Guide](./deployment-guide.md)
- [Integration Architecture](./integration-architecture.md)
