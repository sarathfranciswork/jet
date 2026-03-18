# Source Tree Analysis

**Generated:** 2026-03-18
**Scan Level:** Exhaustive

## Annotated Directory Tree

```
jet/ (plane v0.13.2)
│
├── web/                          # [Part: web] Main Next.js dashboard application
│   ├── pages/                    # Next.js file-based routing (entry points)
│   │   ├── _app.tsx              # App wrapper: MobX, Theme, Toast providers
│   │   ├── _document.tsx         # HTML template: meta, analytics scripts
│   │   ├── index.tsx             # Home/sign-in page
│   │   ├── accounts/             # Auth pages (sign-in, sign-up, password reset, magic link)
│   │   ├── create-workspace.tsx  # Workspace creation flow
│   │   ├── onboarding/           # User onboarding
│   │   ├── invitations/          # Workspace invitation handling
│   │   ├── [workspaceSlug]/      # Workspace-scoped routes
│   │   │   ├── settings/         # Workspace settings (general, members, billing)
│   │   │   ├── projects/         # Projects listing
│   │   │   ├── profile/          # User profile
│   │   │   └── projects/[projectId]/  # Project-scoped routes
│   │   │       ├── issues/       # Issue management (all layouts)
│   │   │       ├── cycles/       # Cycle/sprint management
│   │   │       ├── modules/      # Module management
│   │   │       ├── views/        # Custom saved views
│   │   │       ├── pages/        # Wiki-like pages
│   │   │       ├── inbox/        # Issue inbox/triage
│   │   │       ├── settings/     # Project settings
│   │   │       ├── archived-issues/  # Archived issues
│   │   │       └── draft-issues/     # Draft issues
│   │   └── api/                  # API routes (tracking, Unsplash, Slack)
│   ├── components/               # React components (35 directories, 990+ files)
│   │   ├── issues/               # Issue components (26 subdirs) - largest component group
│   │   │   ├── issue-layouts/    # Multi-layout system (list, kanban, calendar, gantt, spreadsheet)
│   │   │   ├── issue-peek-overview/  # Quick issue preview modal
│   │   │   ├── sidebar-select/   # Issue property selectors
│   │   │   └── sub-issues/       # Sub-issue management
│   │   ├── headers/              # Page headers (25 files, one per page type)
│   │   ├── workspace/            # Workspace components (sidebar, settings)
│   │   ├── project/              # Project components (cards, settings, members)
│   │   ├── cycles/               # Cycle management (20 components)
│   │   ├── modules/              # Module components (14 components)
│   │   ├── ui/                   # Shared UI primitives (27 components)
│   │   ├── core/                 # Core components (activity, modals, filters, theme)
│   │   ├── command-palette/      # Command K interface (9 components)
│   │   ├── analytics/            # Analytics visualizations
│   │   ├── gantt-chart/          # Gantt chart (15 components)
│   │   ├── breadcrumbs/          # Navigation breadcrumbs
│   │   ├── icons/                # Custom SVG icons (91 components)
│   │   ├── notifications/        # Notification UI
│   │   ├── pages/                # Page/wiki components (13 files)
│   │   ├── views/                # Custom view management (9 files)
│   │   └── ...                   # + auth, profile, integration, exporter, DnD, etc.
│   ├── store/                    # MobX state management (20 directories, 50+ stores)
│   │   ├── root.ts               # Root store aggregator
│   │   ├── user.store.ts         # User state & permissions
│   │   ├── theme.store.ts        # Theme & sidebar state
│   │   ├── issue/                # Issue stores (8 stores: CRUD, filters, kanban, calendar, draft)
│   │   ├── workspace/            # Workspace stores (3 stores)
│   │   ├── project/              # Project stores (6 stores: state, label, estimates, publish)
│   │   ├── cycle/                # Cycle stores (8 stores)
│   │   ├── module/               # Module stores (8 stores)
│   │   ├── project-view/         # Project view stores (7 stores)
│   │   ├── global-view/          # Global view stores (6 stores)
│   │   ├── inbox/                # Inbox stores (4 stores)
│   │   └── editor/               # Editor stores (mentions)
│   ├── services/                 # API service layer (21+ services)
│   │   ├── api.service.ts        # Base API class (axios wrapper)
│   │   ├── project/              # Project-specific services (9 services)
│   │   ├── issue/                # Issue-specific services (10 services)
│   │   └── integrations/         # Third-party integration services
│   ├── contexts/                 # React Context providers (6 contexts)
│   ├── hooks/                    # Custom React hooks (19 hooks)
│   ├── layouts/                  # Layout wrappers (app, auth, settings, profile, default)
│   ├── helpers/                  # Utility functions (16 helpers)
│   ├── constants/                # App constants (22 files, incl. 15K+ line fetch-keys)
│   ├── types/                    # TypeScript types (23 files, 3364 lines)
│   ├── styles/                   # CSS/Tailwind styles (5 files)
│   ├── lib/                      # Library utilities (MobX setup)
│   ├── public/                   # Static assets (icons, images, logos)
│   ├── package.json              # Dependencies & scripts
│   ├── next.config.js            # Next.js config (Sentry, image domains)
│   ├── tsconfig.json             # TypeScript config
│   └── tailwind.config.js        # Tailwind CSS config
│
├── space/                        # [Part: space] Public sharing Next.js app
│   ├── pages/                    # Routes: login, onboarding, [workspace]/[project]
│   ├── components/               # Components (7 directories)
│   │   ├── accounts/             # Auth components (sign-in, OAuth)
│   │   ├── issues/               # Issue display (navbar, board-views, peek-overview, filters)
│   │   │   ├── board-views/      # List, kanban, calendar, spreadsheet, gantt views
│   │   │   └── peek-overview/    # Issue detail modal with comments, reactions, votes
│   │   ├── views/                # Page views (login, project-details)
│   │   └── ui/                   # UI primitives (button, input, loader, tooltip)
│   ├── store/                    # MobX stores (root, user, project, issue, issue_detail)
│   ├── services/                 # API services (api, issue, user, project, auth, file)
│   ├── contexts/                 # Toast context
│   ├── hooks/                    # Custom hooks (toast, outside-click, timer)
│   ├── helpers/                  # Helpers
│   ├── constants/                # Constants
│   ├── types/                    # TypeScript types
│   ├── layouts/                  # Layouts
│   └── Configuration files       # package.json, next.config.js, tsconfig.json
│
├── apiserver/                    # [Part: apiserver] Django REST API backend
│   ├── plane/                    # Main Django project
│   │   ├── db/                   # Database layer
│   │   │   ├── models/           # Django ORM models (24+ models)
│   │   │   │   ├── base.py       # BaseModel (UUID pk, audit fields)
│   │   │   │   ├── user.py       # Custom User model
│   │   │   │   ├── workspace.py  # Workspace, WorkspaceMember, Team
│   │   │   │   ├── project.py    # Project, ProjectMember
│   │   │   │   ├── issue.py      # Issue, IssueActivity, IssueAssignee, Labels, Links
│   │   │   │   ├── state.py      # State (issue status groups)
│   │   │   │   ├── cycle.py      # Cycle (sprint), CycleIssue
│   │   │   │   ├── module.py     # Module, ModuleMember, ModuleIssue
│   │   │   │   ├── view.py       # GlobalView, IssueView
│   │   │   │   ├── page.py       # Page, PageBlock
│   │   │   │   ├── inbox.py      # Inbox, InboxIssue
│   │   │   │   ├── estimate.py   # Estimate, EstimatePoint
│   │   │   │   ├── notification.py # Notification
│   │   │   │   ├── api_token.py  # APIToken
│   │   │   │   ├── asset.py      # FileAsset
│   │   │   │   └── integration/  # GitHub, Slack sync models
│   │   │   ├── migrations/       # 46+ migration files
│   │   │   └── management/commands/  # wait_for_db
│   │   ├── api/                  # REST API layer
│   │   │   ├── views/            # 28+ view files (100+ endpoints)
│   │   │   ├── urls/             # 24+ URL config files
│   │   │   ├── serializers/      # 23+ serializer files (89 serializer classes)
│   │   │   └── permissions/      # Workspace & Project permission classes
│   │   ├── bgtasks/              # Celery background tasks (15+ task files)
│   │   ├── settings/             # Multi-environment Django settings
│   │   │   ├── common.py         # Shared settings (39 installed apps)
│   │   │   ├── production.py     # Production (PostgreSQL, S3, Sentry)
│   │   │   ├── local.py          # Local development
│   │   │   ├── selfhosted.py     # Self-hosted deployment
│   │   │   └── test.py           # Test configuration
│   │   ├── utils/                # Utilities (filters, search, grouping, HTML, pagination)
│   │   │   ├── integrations/     # GitHub API helpers
│   │   │   └── importers/        # Jira import utility
│   │   ├── middleware/           # Custom middleware
│   │   └── tests/                # Test suite (10+ test files)
│   ├── templates/emails/         # Email templates (auth, invitations, exports)
│   ├── requirements/             # Python dependencies (base, prod, staging, test, local)
│   ├── manage.py                 # Django CLI entry point
│   └── gunicorn.config.py        # WSGI server config
│
├── packages/                     # [Part: packages] Shared TypeScript libraries
│   ├── ui/                       # @plane/ui - Component library
│   │   └── src/                  # Exported components (Avatar, Breadcrumbs, Button, etc.)
│   ├── editor/                   # Editor packages
│   │   ├── core/                 # @plane/editor-core (TipTap base)
│   │   ├── rich-text-editor/     # @plane/rich-text-editor (full editor)
│   │   └── lite-text-editor/     # @plane/lite-text-editor (comment editor)
│   ├── eslint-config-custom/     # Shared ESLint rules
│   ├── tailwind-config-custom/   # Shared Tailwind config
│   └── tsconfig/                 # Shared TypeScript configs (base, nextjs, react-library)
│
├── deploy/                       # [Part: infra] Deployment configs
│   └── selfhost/                 # Self-hosting (docker-compose, install.sh, variables.env)
├── nginx/                        # Nginx reverse proxy
│   ├── nginx.conf.template       # Proxy config (routes to web, api, space, minio)
│   └── Dockerfile                # Nginx Docker image
├── .github/workflows/            # CI/CD pipelines
│   ├── build-test-pull-request.yml  # PR build validation
│   ├── create-sync-pr.yml          # CE → EE sync
│   └── update-docker-images.yml    # Docker Hub release publishing
│
├── docker-compose.yml            # Development Docker setup (all services)
├── docker-compose-local.yml      # Local dev (external services only)
├── Dockerfile                    # Production multi-stage build
├── turbo.json                    # Turbo monorepo pipeline config
├── package.json                  # Root Yarn workspace config
├── yarn.lock                     # Dependency lockfile
├── setup.sh                      # Development setup script
├── start.sh                      # Node.js start script
├── app.json                      # Heroku app manifest
├── heroku.yml                    # Heroku Docker deployment
├── README.md                     # Project readme
├── CONTRIBUTING.md               # Contribution guidelines
├── ENV_SETUP.md                  # Environment variable reference
├── CODE_OF_CONDUCT.md            # Code of conduct
└── LICENSE.txt                   # AGPL-3.0 license
```

## Critical Folders

| Folder | Purpose | Key Entry Points |
|--------|---------|-----------------|
| `web/pages/` | Next.js routes | `_app.tsx`, `index.tsx`, `[workspaceSlug]/` |
| `web/components/issues/` | Core issue UI | `issue-layouts/`, `issue-peek-overview/` |
| `web/store/` | MobX state | `root.ts` aggregates all stores |
| `web/services/` | API client | `api.service.ts` base class |
| `apiserver/plane/db/models/` | Data models | `__init__.py` registers all models |
| `apiserver/plane/api/views/` | API endpoints | `base.py` for BaseViewSet |
| `apiserver/plane/api/urls/` | URL routing | `__init__.py` aggregates all routes |
| `apiserver/plane/bgtasks/` | Background tasks | Celery tasks for email, notifications, imports |
| `apiserver/plane/settings/` | Django config | `common.py` shared, `production.py` prod |
| `packages/ui/src/` | Shared UI | `index.ts` exports all components |
| `packages/editor/core/` | Editor base | TipTap extensions and hooks |
| `nginx/` | Reverse proxy | `nginx.conf.template` for routing |

## Integration Points Between Parts

```
web/ ──────────── REST API ──────────── apiserver/
  └─ services/*.ts  ─→  HTTP  ─→  plane/api/views/*.py

space/ ─────────── Public API ──────── apiserver/
  └─ services/*.ts  ─→  HTTP  ─→  plane/api/views/ (public endpoints)

web/ & space/ ──── Shared Code ─────── packages/
  └─ import from @plane/ui, @plane/editor-*

nginx/ ────────── Reverse Proxy ────── web/, space/, apiserver/, MinIO
  └─ Routes: / → web, /api/ → api, /spaces/ → space, /uploads/ → minio
```
