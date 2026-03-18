# Integration Architecture

**Generated:** 2026-03-18

## System Architecture Overview

```
                    ┌──────────────┐
                    │   Browser    │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │    Nginx     │  (port 80)
                    │  Rev. Proxy  │
                    └──┬───┬───┬───┘
                       │   │   │
          ┌────────────┘   │   └────────────┐
          │                │                │
   ┌──────▼──────┐  ┌─────▼──────┐  ┌──────▼──────┐
   │  Web App    │  │  API Server │  │  Space App  │
   │  (Next.js)  │  │  (Django)   │  │  (Next.js)  │
   │  port 3000  │  │  port 8000  │  │  port 4000  │
   └──────┬──────┘  └──┬──┬──┬───┘  └──────┬──────┘
          │             │  │  │             │
          └─── REST ────┘  │  └──── REST ───┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼──────┐ ┌──▼────┐ ┌─────▼──────┐
       │ PostgreSQL  │ │ Redis │ │   MinIO     │
       │   15.2      │ │ 6.2.7 │ │  (S3)      │
       │  port 5432  │ │ 6379  │ │  port 9000  │
       └─────────────┘ └───┬───┘ └────────────┘
                           │
                    ┌──────▼───────┐
                    │    Celery    │
                    │   Workers   │
                    ├─────────────┤
                    │  Celery     │
                    │  Beat       │
                    └─────────────┘
```

## Part-to-Part Communication

### 1. Web App → API Server

**Protocol:** REST over HTTP (axios)
**Authentication:** JWT Bearer tokens stored in cookies
**Base URL:** `{NEXT_PUBLIC_API_BASE_URL}/api/v1/`

**Data Flow:**
```
Web Component
  → MobX Store (action)
    → Service Class (axios call)
      → HTTP Request
        → Nginx proxy (/api/ → port 8000)
          → Django REST Framework View
            → Serializer → Model → PostgreSQL
```

**Key Integration Points:**
- `web/services/api.service.ts` — Base API class with cookie-based JWT auth
- 21+ service classes covering all API endpoints
- SWR for data caching with configurable fetch keys (`web/constants/fetch-keys.ts`)

### 2. Space App → API Server

**Protocol:** REST over HTTP (axios)
**Authentication:** Public endpoints (no auth) + optional JWT for logged-in users
**Base URL:** `{NEXT_PUBLIC_API_BASE_URL}/api/v1/`

**Key Difference:** Space uses **public API endpoints** (`/api/v1/public/...`) that don't require authentication, enabling anonymous viewing of published projects.

**Data Flow:**
```
Space Component
  → MobX Store (action)
    → Service Class
      → HTTP Request
        → Nginx proxy (/api/ → port 8000)
          → Django View (AllowAny permission)
            → Serializer → Model → PostgreSQL
```

### 3. Web/Space → Shared Packages

**Protocol:** Direct npm imports (build-time)
**Package Manager:** Yarn Workspaces + Turbo

**Shared Dependencies:**
| Package | Consumer | Purpose |
|---------|----------|---------|
| `@plane/ui` | web, space | UI components (Button, Avatar, Breadcrumbs, etc.) |
| `@plane/editor-core` | web (via rich/lite editors) | TipTap editor base |
| `@plane/rich-text-editor` | web | Full-featured issue description editor |
| `@plane/lite-text-editor` | web | Lightweight comment editor |
| `eslint-config-custom` | web, space | Shared linting rules |
| `tailwind-config-custom` | web, space | Shared Tailwind configuration |
| `tsconfig` | web, space, packages | Shared TypeScript settings |

**Build Order (Turbo Pipeline):**
```
editor-core → rich-text-editor → web
editor-core → lite-text-editor → web
ui → web
ui → space
```

### 4. Nginx Routing

**Configuration:** `nginx/nginx.conf.template`

| Route Pattern | Upstream | Purpose |
|--------------|----------|---------|
| `/` | `web:3000` | Main dashboard app |
| `/api/` | `api:8000` | Backend REST API |
| `/spaces/` | `space:3000` | Public sharing app |
| `/{BUCKET_NAME}/` | `plane-minio:9000` | File uploads (S3) |

**Security Headers Applied:**
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: no-referrer-when-downgrade`
- `Permissions-Policy: interest-cohort=()`
- `Strict-Transport-Security: max-age=31536000`

**File Upload Limit:** Configurable via `FILE_SIZE_LIMIT` env var (default 5MB).

### 5. API Server Internal Architecture

#### Django → PostgreSQL
- Django ORM with 24+ models
- UUID primary keys throughout
- 46+ migration files
- Connection via `DATABASE_URL` environment variable

#### Django → Redis
- **Session/Cache:** Django cache backend
- **Celery Broker:** Task queue messaging
- **Celery Result Backend:** Task result storage
- Connection via `REDIS_URL` environment variable

#### Django → Celery Workers
- **Broker:** Redis
- **Serializer:** JSON
- **Tasks:** 15+ background task types
- **Beat:** Scheduled tasks (export expiration cleanup)

**Background Task Categories:**
| Task | Trigger | Purpose |
|------|---------|---------|
| `issue_activity` | Issue create/update | Track changes, create activity records |
| `notifications` | Issue changes | Send notifications, handle @mentions |
| `workspace_invitation` | Member invite | Send invitation emails |
| `project_invitation` | Project invite | Send project invite emails |
| `email_verification` | Signup | Send verification emails |
| `magic_link` | Magic link auth | Send magic link codes |
| `forgot_password` | Password reset | Send reset emails |
| `send_welcome` | New user | Send welcome emails |
| `service_importer` | Import trigger | Async GitHub/Jira import |
| `export_issues` | Export request | Generate JSON/CSV/XLSX |
| `delete_old_exporters` | Scheduled (Beat) | Cleanup expired exports |
| `issue_automation` | Scheduled | Auto-archive/close rules |
| `analytic_plot_export` | Export request | Generate analytics data |

#### Django → MinIO (S3)
- **Library:** django-s3-storage + boto3
- **Purpose:** File uploads (issue attachments, user avatars, cover images)
- **Bucket:** Configurable via `AWS_S3_BUCKET_NAME` (default: "uploads")
- **Endpoint:** `AWS_S3_ENDPOINT_URL` (MinIO in dev, AWS S3 in prod)

### 6. External Integrations

#### GitHub Integration
```
User → API Server → GitHub API
  ├── OAuth2 authentication (code exchange)
  ├── Repository listing and selection
  ├── Two-way issue sync
  │   ├── GithubRepositorySync → tracks sync config
  │   ├── GithubIssueSync → maps Plane ↔ GitHub issues
  │   └── GithubCommentSync → syncs comments
  └── Release notes fetching
```

#### Slack Integration
```
User → API Server → Slack API
  ├── Bot installation
  ├── Channel notifications
  └── Project sync (SlackProjectSync model)
```

#### Google OAuth
```
User → Frontend → Google OAuth → API Server
  └── id_token verification via google.oauth2
  └── User creation/login
```

#### OpenAI Integration
```
User → Frontend → API Server → OpenAI API
  └── GPT endpoint for AI-assisted features
  └── Configurable model (GPT-3.5/GPT-4)
```

#### Sentry
```
Frontend (Next.js) → Sentry (error tracking)
Backend (Django) → Sentry (error tracking, capture_exception)
```

#### Email (SMTP)
```
Celery Worker → SMTP Server (SendGrid, etc.)
  └── Invitation emails
  └── Verification emails
  └── Password reset emails
  └── Welcome emails
```

## Environment Variable Dependencies

### Cross-Part Communication
| Variable | Used By | Purpose |
|----------|---------|---------|
| `NEXT_PUBLIC_API_BASE_URL` | web, space | API server URL |
| `NEXT_PUBLIC_DEPLOY_URL` | web | Space app URL |
| `DATABASE_URL` | apiserver | PostgreSQL connection |
| `REDIS_URL` | apiserver | Redis connection |
| `AWS_S3_ENDPOINT_URL` | apiserver, nginx | MinIO/S3 endpoint |
| `AWS_S3_BUCKET_NAME` | apiserver, nginx | Storage bucket |
| `NGINX_PORT` | nginx | Proxy listen port |

### External Service Keys
| Variable | Service | Required |
|----------|---------|----------|
| `OPENAI_API_KEY` | OpenAI GPT | Optional |
| `GITHUB_CLIENT_SECRET` | GitHub OAuth/Sync | Optional |
| `SENTRY_DSN` | Sentry | Optional |
| `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | SMTP | Required for emails |
| `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | MinIO/S3 | Required for uploads |

## Data Flow Diagrams

### Issue Creation Flow
```
1. User fills issue form (web)
2. MobX store calls IssueService.createIssue()
3. POST /api/v1/workspaces/<slug>/projects/<uuid>/issues/
4. Nginx proxies to Django API (port 8000)
5. IssueViewSet.create() validates via IssueCreateSerializer
6. Issue model saved to PostgreSQL
7. post_save signal triggers issue_activity.delay()
8. Celery worker processes:
   a. Creates IssueActivity records
   b. Triggers notifications.delay()
   c. Notification task creates Notification records
   d. If @mentions found, creates IssueMention records
9. Response returned to frontend
10. MobX store updates, component re-renders
```

### Public Project Viewing Flow
```
1. User visits Space app URL
2. Space app loads project settings via public API
3. GET /api/v1/public/workspaces/<slug>/project-boards/<uuid>/settings/
4. Loads issues via GET .../issues/ (no auth required)
5. User can view, react, vote, comment on issues
6. All interactions go through public API endpoints
```
