# Architecture - API Server

**Generated:** 2026-03-18
**Part:** apiserver
**Type:** Django REST Backend

## Overview

The API server is a Django 4.2.5 application providing the complete REST API for Plane. It handles authentication, data persistence, background task processing, email delivery, file storage, and external integrations.

## Technology Stack

| Category | Technology | Version |
|----------|-----------|---------|
| Framework | Django | 4.2.5 |
| REST API | Django REST Framework | 3.14.0 |
| Auth | djangorestframework-simplejwt | 5.3.0 |
| Database | PostgreSQL (psycopg) | 15.2 (3.1.10) |
| Cache/Broker | Redis | 4.6.0 |
| Background Tasks | Celery + django_celery_beat | 5.3.4 + 2.5.0 |
| WebSocket | Django Channels | 4.0.0 |
| OAuth | django-allauth, dj_rest_auth | 0.55.2, 2.2.5 |
| File Storage | django-s3-storage + boto3 | 0.14.0 |
| CORS | django-cors-headers | 4.2.0 |
| Permissions | django-guardian | 2.4.0 |
| Error Tracking | sentry-sdk | 1.30.0 |
| WSGI Server | Gunicorn | 21.2.0 |
| ASGI Server | Uvicorn | 0.23.2 |

## Architecture Pattern

**Layered MVC (Django convention)**

```
URL Router → View (Controller) → Serializer → Model → Database
                ↓                    ↑
            Permission          Validation
                ↓
         Background Task (Celery)
                ↓
     Email / Notification / Import
```

## Application Structure

```
plane/
├── db/          # Data layer (models, migrations, management commands)
├── api/         # API layer (views, serializers, URLs, permissions)
├── bgtasks/     # Celery background tasks
├── settings/    # Multi-environment Django configuration
├── utils/       # Utilities (filters, search, pagination, HTML processing)
├── middleware/   # Custom middleware
├── web/         # Legacy web views
├── analytics/   # Analytics module
└── tests/       # Test suite
```

## Model Layer

24+ Django models organized by domain. All inherit from `BaseModel`:
- UUID primary keys
- Automatic `created_at`, `updated_at` timestamps
- Automatic `created_by`, `updated_by` via `crum` middleware

### Core Domain Models
- **User** — Custom auth model (email-based, OAuth support)
- **Workspace** — Multi-tenant container (Owner/Admin/Member/Guest roles)
- **Project** — Issue container within workspace (configurable features)
- **Issue** — Core entity with rich metadata, sub-issues, relations
- **State** — Issue status with groups (backlog/unstarted/started/completed/cancelled)
- **Label** — Categorization with hierarchy support
- **Cycle** — Time-boxed sprint (issue in max 1 cycle)
- **Module** — Feature grouping (issue can be in multiple modules)
- **Page** — Wiki-like documents with issue-linked blocks
- **View** — Saved filter/display configurations
- **Inbox** — Issue triage queue
- **Estimate** — Story point system

See [Data Models](./data-models-apiserver.md) for complete field-level documentation.

## API Layer

100+ REST endpoints organized by resource. See [API Contracts](./api-contracts-apiserver.md) for complete endpoint documentation.

### Base Classes
- **BaseViewSet** — Extends `ModelViewSet` with timezone handling, pagination, error handling, query logging
- **BaseAPIView** — Extends `APIView` with same mixins

### View Pattern
```python
class ExampleViewSet(BaseViewSet):
    serializer_class = ExampleSerializer
    model = Example
    permission_classes = [ProjectEntityPermission]

    def get_queryset(self):
        return self.filter_queryset(
            super().get_queryset()
            .filter(workspace__slug=self.kwargs["slug"])
        )

    def perform_create(self, serializer):
        serializer.save(project_id=self.kwargs["project_id"])
```

## Permission System

Two-level role-based access control:

### Workspace Level
| Role | Value | Capabilities |
|------|-------|-------------|
| Owner | 20 | Full control, delete workspace |
| Admin | 15 | Manage members, settings, integrations |
| Member | 10 | Read, create projects |
| Guest | 5 | Read-only |

### Project Level
| Role | Value | Capabilities |
|------|-------|-------------|
| Admin | 20 | Full project control |
| Member | 15 | Create/edit issues, cycles, modules |
| Viewer | 10 | Read-only |
| Guest | 5 | Limited read |

## Authentication

### Methods
1. **Email/Password** — SignUp → SignIn → JWT tokens
2. **OAuth** — Google (id_token) / GitHub (code exchange)
3. **Magic Link** — Generate code → Email → Verify
4. **JWT Tokens** — Access (7 days) + Refresh (43200 days), HS256

### Flow
```
Client → POST /auth/sign-in/ → JWT (access + refresh tokens)
Client → Authorization: Bearer <access_token> → API calls
Client → POST /auth/token/refresh/ → New access token
```

## Background Tasks (Celery)

15+ task types processed asynchronously:

| Task | Trigger | Purpose |
|------|---------|---------|
| `issue_activity` | Issue changes | Create IssueActivity audit records |
| `notifications` | Issue changes | Create Notification records, handle @mentions |
| `workspace_invitation` | Member invite | Send email via SMTP |
| `project_invitation` | Project invite | Send email via SMTP |
| `email_verification` | Signup | JWT verification email |
| `magic_link` | Magic link auth | Send magic link code |
| `forgot_password` | Password reset | Reset email with token |
| `send_welcome` | New user | Welcome email |
| `service_importer` | Import trigger | Async GitHub/Jira import |
| `export_issues` | Export request | Generate JSON/CSV/XLSX |
| `delete_old_exporters` | Scheduled (Beat) | Cleanup expired exports |
| `issue_automation` | Scheduled | Auto-archive/close rules |
| `analytic_plot_export` | Export request | Analytics data generation |

## Settings Configuration

Multi-environment settings in `plane/settings/`:

| File | Environment | Database | Key Differences |
|------|-------------|----------|----------------|
| `common.py` | Shared | SQLite (default) | 39 installed apps, JWT config, CORS |
| `local.py` | Development | PostgreSQL | DEBUG=True |
| `production.py` | Production | PostgreSQL | S3 storage, Sentry, SMTP |
| `staging.py` | Staging | PostgreSQL | Similar to production |
| `selfhosted.py` | Self-hosted | PostgreSQL | Simplified config |
| `test.py` | Testing | SQLite | Fast test execution |

## External Integrations

| Service | Library | Purpose |
|---------|---------|---------|
| GitHub | REST API calls | OAuth, repository sync, issue sync |
| Slack | slack-sdk 3.21.3 | Bot notifications, project sync |
| Google | google-auth 2.22.0 | OAuth authentication |
| OpenAI | openai 0.28.0 | AI-powered issue assistance |
| Unsplash | REST API | Cover image search |
| AWS S3 / MinIO | boto3, django-s3-storage | File upload storage |
| Sentry | sentry-sdk 1.30.0 | Error tracking |
| SMTP | Django mail | Transactional emails |

## Key Architectural Patterns

- **Audit Trail:** `crum` middleware auto-captures `created_by`/`updated_by` on every save
- **Signal-Driven Tasks:** `post_save` signals trigger Celery tasks for activity tracking
- **Dynamic Serializers:** `DynamicBaseSerializer` supports field filtering via `?fields=` query param
- **Custom Managers:** `Issue.issue_objects` filters archived/draft by default
- **UUID Everything:** All primary keys are UUIDs for distributed safety
- **JSON Fields:** Extensive use of `JSONField` for flexible metadata (description, view_props, theme, etc.)
