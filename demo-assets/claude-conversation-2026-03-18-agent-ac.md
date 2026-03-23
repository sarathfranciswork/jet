# Claude Conversation Log

Session ID: agent-ac35a0a5b8e30ebef
Date: 2026-03-18 19:26:07

---

## 👤 User

Very thorough exploration of /Users/sarathfrancis/work/git/innovation_lab/jet/apiserver

This is part of an exhaustive documentation scan. I need you to analyze EVERY source file. This is a Django 4.2.5 / Python / DRF / Celery backend API.

Please analyze and report on:

1. **Directory structure**: Full tree of apiserver/
2. **Django models**: Read ALL model files in plane/db/models/ - document every model, its fields, relationships, and Meta options
3. **API endpoints**: Read ALL view files in plane/api/views/ - document every endpoint, HTTP methods, permissions
4. **URL routing**: Read ALL url files in plane/api/urls/ - map complete URL structure
5. **Serializers**: Read key serializers in plane/api/serializers/
6. **Permissions**: Read permission classes in plane/api/permissions/
7. **Background tasks**: Read ALL Celery tasks in plane/bgtasks/
8. **Middleware**: Custom middleware
9. **Settings**: Read common.py, production.py, local.py settings
10. **Authentication**: Auth flow (OAuth, JWT, sessions, django-allauth)
11. **Database migrations**: List all migrations and key schema changes
12. **Management commands**: Custom Django management commands
13. **Utils**: Utility modules
14. **External integrations**: GitHub, Slack, OpenAI, AWS/MinIO, Sentry

For each model, document:
- Model name, fields, field types
- ForeignKey/ManyToMany relationships
- Custom methods
- Related serializers and views

For each API endpoint, document:
- URL path, HTTP methods
- View class/function
- Permission classes
- Request/response format

Return a comprehensive structured report.

---

## 🤖 Claude

I'll conduct a thorough exploration of the `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver` directory. Let me start by mapping the overall structure and then systematically analyze each component.

---

## 🤖 Claude

Let me continue exploring the structure more systematically:

---

## 🤖 Claude

Now let me read all the model files systematically:

---

## 🤖 Claude

Continue reading the remaining model files:

---

## 🤖 Claude

Continue with more models:

---

## 🤖 Claude

Continue with remaining models:

---

## 🤖 Claude

Now let me read the rest of the models and then move on to views, serializers, and other components:

---

## 🤖 Claude

Now let me read the critical issue.py sections I missed, and then move to views and serializers:

---

## 🤖 Claude

Let me read the key views and serializers to understand the API structure:

---

## 🤖 Claude

Let me read some key serializers and views to understand the API structure:

---

## 🤖 Claude

Let me read the URL routing structure and get Celery tasks:

---

## 🤖 Claude

Let me read the Celery task files:

---

## 🤖 Claude

Let me continue reading settings and then get information on migrations and utilities:

---

## 🤖 Claude

Let me continue gathering more information on views and integration models:

---

## 🤖 Claude

Let me get more key integration and serializer information:

---

## 🤖 Claude

Let me get some additional key information about URL patterns and remaining critical components:

---

## 🤖 Claude

Let me gather information on the remaining Celery tasks and check the main urls/wsgi:

---

## 🤖 Claude

Now let me get the complete directory structure and create a comprehensive summary:

---

## 🤖 Claude

Perfect! Now let me compile the comprehensive report. Let me gather a few more key pieces:

---

## 🤖 Claude

Excellent! Now I have gathered comprehensive information. Let me create the detailed report:

## COMPREHENSIVE ANALYSIS REPORT: PLANE APISERVER

### 1. DIRECTORY STRUCTURE

```
apiserver/
├── bin/                              # Binary scripts
│   └── user_script.py
├── plane/                            # Main application directory (Django project)
│   ├── __init__.py
│   ├── asgi.py                       # ASGI config for async support
│   ├── wsgi.py                       # WSGI entry point
│   ├── urls.py                       # Root URL configuration
│   ├── middleware/                   # Custom middleware
│   │   ├── __init__.py
│   │   └── apps.py
│   ├── settings/                     # Django settings (multi-environment)
│   │   ├── __init__.py
│   │   ├── common.py                 # Shared settings
│   │   ├── production.py
│   │   ├── staging.py
│   │   ├── local.py                  # Local development
│   │   ├── test.py
│   │   ├── selfhosted.py
│   │   └── redis.py
│   ├── db/                           # Database models and migrations
│   │   ├── models/                   # 24+ model files (225 total Python files)
│   │   │   ├── __init__.py
│   │   │   ├── base.py               # BaseModel with UUID pk & audit trail
│   │   │   ├── user.py               # User model (custom auth)
│   │   │   ├── workspace.py          # Workspace, WorkspaceMember, Team
│   │   │   ├── project.py            # Project, ProjectMember, ProjectIdentifier
│   │   │   ├── issue.py              # Issue, IssueActivity, IssueAssignee, Labels
│   │   │   ├── state.py              # State (issue status)
│   │   │   ├── cycle.py              # Cycle (sprint), CycleIssue
│   │   │   ├── module.py             # Module, ModuleMember, ModuleIssue
│   │   │   ├── view.py               # GlobalView, IssueView
│   │   │   ├── page.py               # Page, PageBlock (wiki-like)
│   │   │   ├── inbox.py              # Inbox, InboxIssue
│   │   │   ├── estimate.py           # Estimate, EstimatePoint (story points)
│   │   │   ├── notification.py       # Notification model
│   │   │   ├── api_token.py          # APIToken for bot/service auth
│   │   │   ├── asset.py              # FileAsset (S3 file uploads)
│   │   │   ├── social_connection.py  # OAuth connections (Google, GitHub)
│   │   │   ├── analytic.py           # AnalyticView
│   │   │   ├── importer.py           # Importer (GitHub, Jira)
│   │   │   ├── exporter.py           # ExporterHistory
│   │   │   └── integration/          # Third-party integrations
│   │   │       ├── base.py
│   │   │       ├── github.py         # GitHub sync models
│   │   │       └── slack.py          # Slack sync models
│   │   ├── migrations/               # Database migrations (~46 files)
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── wait_for_db.py    # Startup health check
│   │   ├── mixins.py                 # AuditModel mixin (created_by, updated_by)
│   │   └── apps.py
│   ├── api/                          # REST API endpoints
│   │   ├── views/                    # 28+ view files (APIView/ViewSet classes)
│   │   │   ├── base.py               # BaseViewSet, BaseAPIView, error handling
│   │   │   ├── authentication.py     # SignUp, SignIn, OAuth, MagicLink
│   │   │   ├── auth_extended.py      # Email verification, password reset
│   │   │   ├── workspace.py          # Workspace CRUD, members, invites
│   │   │   ├── project.py            # Project CRUD, members
│   │   │   ├── issue.py              # Issue CRUD (large file)
│   │   │   ├── cycle.py              # Cycle management
│   │   │   ├── module.py             # Module management
│   │   │   ├── state.py              # Issue state/status
│   │   │   ├── view.py               # Custom views/filters
│   │   │   ├── page.py               # Wiki pages
│   │   │   ├── inbox.py              # Inbox features
│   │   │   ├── estimate.py           # Estimates
│   │   │   ├── notification.py       # Notifications
│   │   │   ├── user.py               # User profile
│   │   │   ├── asset.py              # File uploads
│   │   │   ├── api_token.py          # API tokens
│   │   │   ├── analytic.py           # Analytics
│   │   │   ├── importer.py           # Import services
│   │   │   ├── exporter.py           # Export issues
│   │   │   ├── oauth.py              # OAuth handling (Google, GitHub)
│   │   │   ├── search.py             # Global search
│   │   │   ├── config.py             # Configuration endpoints
│   │   │   ├── external.py           # GPT, Unsplash, Release notes
│   │   │   └── integration/          # Integration endpoints
│   │   │       ├── github.py         # GitHub sync endpoints
│   │   │       └── slack.py          # Slack sync endpoints
│   │   ├── urls/                     # 24+ URL configuration files
│   │   │   ├── __init__.py           # Main URL aggregator
│   │   │   ├── authentication.py     # Auth routes
│   │   │   ├── workspace.py          # Workspace routes
│   │   │   ├── project.py            # Project routes
│   │   │   ├── issue.py              # Issue routes
│   │   │   ├── cycle.py              # Cycle routes
│   │   │   ├── module.py             # Module routes
│   │   │   ├── view.py               # View routes
│   │   │   ├── state.py              # State routes
│   │   │   ├── page.py               # Page routes
│   │   │   ├── inbox.py              # Inbox routes
│   │   │   ├── notification.py       # Notification routes
│   │   │   ├── estimate.py           # Estimate routes
│   │   │   ├── asset.py              # Asset routes
│   │   │   ├── api_token.py          # Token routes
│   │   │   ├── integration.py        # Integration routes
│   │   │   ├── importer.py           # Importer routes
│   │   │   ├── exporter.py           # Exporter routes
│   │   │   ├── analytic.py           # Analytics routes
│   │   │   ├── search.py             # Search routes
│   │   │   ├── configuration.py      # Config routes
│   │   │   ├── gpt.py                # GPT routes
│   │   │   ├── unsplash.py           # Unsplash routes
│   │   │   ├── public_board.py       # Public board routes
│   │   │   └── release_note.py       # Release notes routes
│   │   ├── serializers/              # 23+ serializer files
│   │   │   ├── base.py               # BaseSerializer, DynamicBaseSerializer
│   │   │   ├── user.py               # UserSerializer, UserLiteSerializer
│   │   │   ├── workspace.py          # WorkspaceSerializer, Members
│   │   │   ├── project.py            # ProjectSerializer, Members
│   │   │   ├── issue.py              # Issue serializers (IssueFlatSerializer, IssueCreateSerializer)
│   │   │   ├── state.py              # StateSerializer
│   │   │   ├── cycle.py              # CycleSerializer
│   │   │   ├── module.py             # ModuleSerializer
│   │   │   ├── view.py               # ViewSerializer
│   │   │   ├── page.py               # PageSerializer
│   │   │   ├── inbox.py              # InboxSerializer
│   │   │   ├── estimate.py           # EstimateSerializer
│   │   │   ├── notification.py       # NotificationSerializer
│   │   │   ├── api_token.py          # APITokenSerializer
│   │   │   ├── asset.py              # FileAssetSerializer
│   │   │   ├── analytic.py           # AnalyticSerializer
│   │   │   ├── importer.py           # ImporterSerializer
│   │   │   ├── exporter.py           # ExporterSerializer
│   │   │   └── integration/          # Integration serializers
│   │   │       ├── base.py
│   │   │       ├── github.py
│   │   │       └── slack.py
│   │   ├── permissions/              # Custom permission classes
│   │   │   ├── workspace.py          # Workspace permissions (Owner/Admin/Member/Guest)
│   │   │   └── project.py            # Project permissions (Admin/Member/Viewer)
│   │   └── __init__.py
│   ├── bgtasks/                      # Celery background tasks (15+ files)
│   │   ├── issue_activites_task.py   # Track issue changes
│   │   ├── notification_task.py      # Send notifications
│   │   ├── workspace_invitation_task.py   # Invite emails
│   │   ├── project_invitation_task.py    # Project invites
│   │   ├── email_verification_task.py    # Email verification
│   │   ├── magic_link_code_task.py       # Magic link auth
│   │   ├── forgot_password_task.py       # Password reset emails
│   │   ├── user_welcome_task.py          # Welcome emails
│   │   ├── importer_task.py              # Service imports (async)
│   │   ├── export_task.py                # Issue exports
│   │   ├── exporter_expired_task.py      # Export expiration
│   │   ├── issue_automation_task.py      # Issue automation
│   │   ├── analytic_plot_export.py       # Analytics exports
│   │   ├── apps.py
│   │   └── __init__.py
│   ├── utils/                        # Utility modules
│   │   ├── issue_filters.py          # Issue query filtering
│   │   ├── issue_search.py           # Issue search functionality
│   │   ├── grouper.py                # Result grouping
│   │   ├── html_processor.py         # HTML sanitization
│   │   ├── markdown.py               # Markdown processing
│   │   ├── analytics_plot.py         # Analytics plotting
│   │   ├── paginator.py              # Custom pagination
│   │   ├── ip_address.py             # IP utilities
│   │   ├── imports.py                # Import utilities
│   │   ├── integrations/             # Integration helpers
│   │   │   ├── __init__.py
│   │   │   └── github.py             # GitHub API integration
│   │   ├── importers/                # Service importers
│   │   │   ├── __init__.py
│   │   │   └── jira.py               # Jira importer
│   │   └── __init__.py
│   ├── web/                          # Web serving (static files, etc)
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── apps.py
│   │   └── __init__.py
│   ├── analytics/                    # Analytics module
│   ├── tests/                        # Test suite (~10 test files)
│   │   ├── api/
│   │   │   ├── test_authentication.py
│   │   │   ├── test_auth_extended.py
│   │   │   ├── test_workspace.py
│   │   │   ├── test_project.py
│   │   │   ├── test_issue.py
│   │   │   ├── test_cycle.py
│   │   │   ├── test_view.py
│   │   │   ├── test_module.py
│   │   │   ├── test_state.py
│   │   │   ├── test_people.py
│   │   │   ├── test_asset.py
│   │   │   ├── test_oauth.py
│   │   │   ├── test_shortcut.py
│   │   │   └── base.py
│   │   └── __init__.py
│   └── static/                       # Static files (CSS, JS)
│       ├── css/
│       └── js/
├── templates/                        # Email templates
│   ├── emails/
│   │   ├── auth/
│   │   ├── exports/
│   │   ├── invitations/
│   │   └── admin/
├── manage.py                         # Django CLI
├── gunicorn.config.py                # Gunicorn config
├── Dockerfile.api                    # Production Docker image
├── Dockerfile.dev                    # Development Docker image
├── Procfile                          # Heroku process file
├── requirements/                     # Python dependencies
│   ├── base.txt                      # Core dependencies
│   ├── production.txt
│   ├── staging.txt
│   ├── test.txt
│   └── local.txt
├── back_migration.py                 # Migration utility
├── runtime.txt                       # Python runtime version
└── .env.example                      # Environment variables template
```

### 2. DJANGO MODELS (24+ Models)

#### Core Models:

**User Model** (`plane/db/models/user.py`)
- Custom user extending AbstractBaseUser, PermissionsMixin
- Fields: UUID pk, email, username, mobile_number, avatar, cover_image, timezone
- Auth tracking: last_login_time, last_login_ip, last_login_medium, token
- Flags: is_superuser, is_staff, is_active, is_email_verified, is_onboarded, is_tour_completed
- Business fields: billing_address, display_name, my_issues_prop, onboarding_step
- Signal: Sends Slack notification on user signup

**Workspace** (`plane/db/models/workspace.py`)
- Fields: name, logo, slug (unique), owner (FK User), organization_size
- Relations: WorkspaceMember (M2M through), Team (O2M), WorkspaceTheme
- Role hierarchy for members: Owner(20), Admin(15), Member(10), Guest(5)
- Default props for issue filtering, display, and layout

**WorkspaceMember**
- Unique together: [workspace, member]
- Role: PositiveSmallIntegerField (choices)
- Stores: view_props, default_props, issue_props (JSON)

**WorkspaceMemberInvite**
- Unique together: [email, workspace]
- Fields: email, token, accepted, message, responded_at, role
- Supports invitation lifecycle with expiration tracking

**Team**
- Unique together: [name, workspace]
- M2M Members through TeamMember
- Description, workspace FK

**Project** (`plane/db/models/project.py`)
- Fields: name, identifier (like PROJ), description, workspace FK
- Network: choices (0=Secret, 2=Public)
- Features: module_view, cycle_view, issue_views_view, page_view, inbox_view
- Defaults: default_assignee, project_lead, default_state
- Estimate: FK to Estimate model
- Archive/Close policies: archive_in, close_in (0-12 months)

**ProjectMember**
- Role: Admin(20), Member(15), Viewer(10), Guest(5)
- Stores: view_props, default_props, preferences, sort_order
- Unique together: [project, member]

**ProjectIdentifier**
- OneToOne with Project
- Unique together: [name, workspace]

**Issue** (`plane/db/models/issue.py`)
- Fields: name, description (JSON), priority (choices), state FK
- Dates: start_date, target_date, completed_at, archived_at
- M2M: assignees (through IssueAssignee), labels (through IssueLabel)
- Tracking: sequence_id, sort_order, is_draft, parent (self FK for sub-issues)
- Custom manager: issue_objects filters out archived/draft issues
- Signal: Auto-completes when state changes to "completed"

**IssueActivity** (`plane/db/models/issue.py`)
- Verb: verb (created/updated)
- Field tracking: field, old_value, new_value
- Relations: issue FK, actor (User FK), issue_comment FK
- Epoch: float timestamp for grouping activities

**IssueAssignee, IssueLabel, IssueLink, IssueAttachment**
- Support M2M relationships through table models
- IssueAttachment: file uploads with validators, metadata

**State** (`plane/db/models/state.py`)
- Unique together: [name, project]
- Group: backlog/unstarted/started/completed/cancelled
- Color, sequence, default flag
- Auto-generates slug from name

**Cycle** (`plane/db/models/cycle.py`)
- Fields: name, description, start_date, end_date
- owned_by: User FK
- view_props, sort_order (auto-calculated on creation)
- Relations: CycleIssue (O2O with Issue), CycleFavorite

**Module** (`plane/db/models/module.py`)
- Fields: name, description, status, lead
- Dates: start_date, target_date
- M2M: members (through ModuleMember)
- Relations: ModuleIssue (O2O), ModuleLink (external URLs), ModuleFavorite

**View** (`plane/db/models/view.py`)
- GlobalView: workspace-level custom views
- IssueView: project-level custom views
- Fields: name, description, query (JSON), access (0=Private, 1=Public), query_data

**Page** (`plane/db/models/page.py`)
- Fields: name, description (JSON), color, owned_by (User FK)
- Access: 0=Public, 1=Private
- Relations: PageBlock (O2M for page content), PageLabel, PageFavorite

**PageBlock**
- Represents content blocks in a page
- Links to Issue via issue FK (sync-able)
- Tracks: completed_at, sort_order, sync flag

**Inbox** (`plane/db/models/inbox.py`)
- name, description, is_default, view_props
- Unique together: [name, project]
- Relations: InboxIssue (O2M)

**InboxIssue**
- Status: -2=Pending, -1=Rejected, 0=Snoozed, 1=Accepted, 2=Duplicate
- snoozed_till, duplicate_to (FK to Issue)
- source field for tracking origin

**Estimate** (`plane/db/models/estimate.py`)
- Unique together: [name, project]
- EstimatePoint: key (0-7), value, description

**Notification** (`plane/db/models/notification.py`)
- Fields: title, message (JSON), sender, entity_identifier, entity_name
- Relations: workspace, project, triggered_by (User), receiver (User)
- Tracking: read_at, snoozed_till, archived_at

**APIToken** (`plane/db/models/api_token.py`)
- token: unique generated token (UUID hex * 2)
- label: generated label
- user_type: 0=Human, 1=Bot
- user FK, workspace FK

**FileAsset** (`plane/db/models/asset.py`)
- asset: FileField with S3 upload_to path
- attributes: JSON metadata
- workspace FK (nullable for user assets)
- Validator: file_size (max 5MB configurable)

**SocialLoginConnection** (`plane/db/models/social_connection.py`)
- medium: Google or GitHub
- user FK
- token_data, extra_data (JSON)
- last_login_at, last_received_at

**Integration Models** (`plane/db/models/integration/`)

**GithubRepository**
- name, url, repository_id, owner
- config: JSON for sync settings
- Unique together: implicit on project + repo_id

**GithubRepositorySync**
- repository (O2O), actor (User), workspace_integration FK
- credentials, label FK
- Tracks repository syncing state

**GithubIssueSync**
- repo_issue_id, github_issue_id, issue_url
- issue FK, repository_sync FK
- Unique together: [repository_sync, issue]

**SlackProjectSync**
- access_token, scopes, bot_user_id, webhook_url
- team_id, team_name, data (JSON)
- workspace_integration FK
- Unique together: [team_id, project]

**Importer** (`plane/db/models/importer.py`)
- service: github/jira
- status: queued/processing/completed/failed
- initiated_by (User), token (APIToken), metadata, config, data, imported_data (JSON)

**ExporterHistory** (`plane/db/models/exporter.py`)
- provider: json/csv/xlsx
- status: queued/processing/completed/failed
- projects: ArrayField of UUIDs
- url, key (storage path), token

**AnalyticView** (`plane/db/models/analytic.py`)
- name, description, query (JSON), query_dict
- workspace FK

### 3. API ENDPOINTS & VIEWS

Base Classes:
- **BaseViewSet**: extends ModelViewSet, includes timezone handling, pagination, error handling, query logging
- **BaseAPIView**: extends APIView, same mixins as BaseViewSet

#### Authentication Endpoints
- `POST /auth/sign-up/` - SignUpEndpoint (AllowAny)
- `POST /auth/sign-in/` - SignInEndpoint (AllowAny)
- `POST /auth/sign-out/` - SignOutEndpoint
- `POST /auth/magic-generate/` - MagicSignInGenerateEndpoint (AllowAny)
- `POST /auth/magic-sign-in/` - MagicSignInEndpoint (AllowAny)
- `POST /auth/social-auth/` - OauthEndpoint (AllowAny) [Google, GitHub]
- `POST /auth/token/refresh/` - TokenRefreshView (JWT)
- `GET /auth/email-verify/` - VerifyEmailEndpoint
- `GET /auth/request-email-verify/` - RequestEmailVerificationEndpoint
- `POST /auth/forgot-password/` - ForgotPasswordEndpoint (AllowAny)
- `POST /auth/reset-password/<uidb64>/<token>/` - ResetPasswordEndpoint
- `PATCH /auth/users/me/change-password/` - ChangePasswordEndpoint
- `POST /auth/api-tokens/` - ApiTokenEndpoint (CRUD)

#### Workspace Endpoints
- `GET/POST /workspaces/` - WorkSpaceViewSet
- `GET/PUT/PATCH/DELETE /workspaces/<slug>/` - WorkSpaceViewSet detail
- `POST /workspaces/<slug>/invite/` - InviteWorkspaceEndpoint
- `GET /workspaces/<slug>/invitations/` - WorkspaceInvitationsViewset
- `GET/POST /workspaces/<slug>/members/` - WorkSpaceMemberViewSet
- `GET/PATCH/DELETE /workspaces/<slug>/members/<uuid>/` - WorkSpaceMemberViewSet detail
- `GET /workspaces/<slug>/members/me/` - WorkspaceMemberUserEndpoint
- `GET /workspaces/slug-check/` - WorkSpaceAvailabilityCheckEndpoint
- `GET /workspaces/<slug>/themes/` - WorkspaceThemeViewSet (CRUD)
- `POST /workspaces/<slug>/leave/` - LeaveWorkspaceEndpoint
- `GET /workspaces/<slug>/labels/` - WorkspaceLabelsEndpoint
- `GET /workspaces/<slug>/user-profile/` - WorkspaceUserProfileEndpoint
- `GET /workspaces/<slug>/user-profile-stats/` - WorkspaceUserProfileStatsEndpoint
- `GET /workspaces/<slug>/user-activity/` - WorkspaceUserActivityEndpoint
- `GET /workspaces/<slug>/user-profile-issues/` - WorkspaceUserProfileIssuesEndpoint

#### Project Endpoints
- `GET/POST /workspaces/<slug>/projects/` - ProjectViewSet
- `GET/PUT/PATCH/DELETE /workspaces/<slug>/projects/<uuid>/` - ProjectViewSet detail
- `GET /workspaces/<slug>/project-identifiers/` - ProjectIdentifierEndpoint
- `POST /workspaces/<slug>/projects/<uuid>/invite/` - InviteProjectEndpoint
- `GET/POST /workspaces/<slug>/projects/<uuid>/members/` - ProjectMemberViewSet
- `GET/PATCH/DELETE /workspaces/<slug>/projects/<uuid>/members/<uuid>/` - ProjectMemberViewSet detail
- `POST /workspaces/<slug>/projects/join/` - ProjectJoinEndpoint
- `POST /workspaces/<slug>/projects/<uuid>/team-invite/` - AddTeamToProjectEndpoint
- `GET /workspaces/<slug>/projects/<uuid>/invitations/` - ProjectMemberInvitationsViewset
- `GET /workspaces/<slug>/projects/<uuid>/favorites/` - ProjectFavoritesViewSet

#### Issue Endpoints
- `GET/POST /workspaces/<slug>/projects/<uuid>/issues/` - IssueViewSet
- `GET/PUT/PATCH/DELETE /workspaces/<slug>/projects/<uuid>/issues/<uuid>/` - IssueViewSet detail
- `GET /workspaces/<slug>/my-issues/` - UserWorkSpaceIssues
- `POST /workspaces/<slug>/projects/<uuid>/issues/<uuid>/sub-issues/` - SubIssuesEndpoint
- `GET/POST /workspaces/<slug>/projects/<uuid>/issues/<uuid>/issue-links/` - IssueLinkViewSet
- `POST /workspaces/<slug>/projects/<uuid>/bulk-delete-issues/` - BulkDeleteIssuesEndpoint
- `POST /workspaces/<slug>/projects/<uuid>/bulk-create-labels/` - BulkCreateIssueLabelsEndpoint
- `POST /workspaces/<slug>/projects/<uuid>/bulk-import-issues/<service>/` - BulkImportIssuesEndpoint
- `GET /workspaces/<slug>/projects/<uuid>/issues/<uuid>/activity/` - IssueActivityEndpoint
- `GET/POST /workspaces/<slug>/projects/<uuid>/issues/<uuid>/comments/` - IssueCommentViewSet
- `GET/POST /workspaces/<slug>/projects/<uuid>/issues/<uuid>/subscribers/` - IssueSubscriberViewSet
- `GET/POST /workspaces/<slug>/projects/<uuid>/issues/<uuid>/reactions/` - IssueReactionViewSet
- `GET/POST /workspaces/<slug>/projects/<uuid>/comments/<uuid>/reactions/` - CommentReactionViewSet
- `GET/POST /workspaces/<slug>/projects/<uuid>/issue-labels/` - LabelViewSet
- `POST /workspaces/<slug>/projects/<uuid>/export-issues/` - ExportIssuesEndpoint
- `GET /workspaces/<slug>/projects/<uuid>/archived-issues/` - IssueArchiveViewSet
- `GET/POST /workspaces/<slug>/projects/<uuid>/issue-relations/` - IssueRelationViewSet
- `GET /workspaces/<slug>/projects/<uuid>/draft-issues/` - IssueDraftViewSet

#### Cycle Endpoints
- `GET/POST /workspaces/<slug>/projects/<uuid>/cycles/` - CycleViewSet
- `GET/PUT/PATCH/DELETE /workspaces/<slug>/projects/<uuid>/cycles/<uuid>/` - CycleViewSet detail
- `GET/POST /workspaces/<slug>/projects/<uuid>/cycle-issues/` - CycleIssueViewSet
- `DELETE /workspaces/<slug>/projects/<uuid>/cycle-issues/<uuid>/` - CycleIssueViewSet delete
- `POST /workspaces/<slug>/projects/<uuid>/cycles/<uuid>/date-check/` - CycleDateCheckEndpoint
- `GET/POST /workspaces/<slug>/projects/<uuid>/cycle-favorites/` - CycleFavoriteViewSet
- `POST /workspaces/<slug>/projects/<uuid>/cycles/<uuid>/transfer-issues/` - TransferCycleIssueEndpoint

#### Module Endpoints
- `GET/POST /workspaces/<slug>/projects/<uuid>/modules/` - ModuleViewSet
- `GET/PATCH/DELETE /workspaces/<slug>/projects/<uuid>/modules/<uuid>/` - ModuleViewSet detail
- `GET/POST /workspaces/<slug>/projects/<uuid>/module-issues/` - ModuleIssueViewSet
- `GET/POST /workspaces/<slug>/projects/<uuid>/module-members/` - ModuleMemberViewSet
- `GET/POST /workspaces/<slug>/projects/<uuid>/module-links/` - ModuleLinkViewSet
- `GET/POST /workspaces/<slug>/projects/<uuid>/module-favorites/` - ModuleFavoriteViewSet

#### State Endpoints
- `GET/POST /workspaces/<slug>/projects/<uuid>/states/` - StateViewSet
- `GET/PUT/PATCH/DELETE /workspaces/<slug>/projects/<uuid>/states/<uuid>/` - StateViewSet detail

#### View Endpoints
- `GET/POST /workspaces/<slug>/projects/<uuid>/views/` - IssueViewSet
- `GET/PATCH/DELETE /workspaces/<slug>/projects/<uuid>/views/<uuid>/` - IssueViewSet detail
- `GET/POST /workspaces/<slug>/projects/<uuid>/view-favorites/` - IssueViewFavoriteViewSet

#### Page Endpoints
- `GET/POST /workspaces/<slug>/projects/<uuid>/pages/` - PageViewSet
- `GET/PATCH/DELETE /workspaces/<slug>/projects/<uuid>/pages/<uuid>/` - PageViewSet detail
- `GET/POST /workspaces/<slug>/projects/<uuid>/page-blocks/` - PageBlockViewSet
- `GET/POST /workspaces/<slug>/projects/<uuid>/page-favorites/` - PageFavoriteViewSet

#### Inbox Endpoints
- `GET/POST /workspaces/<slug>/projects/<uuid>/inbox/` - InboxViewSet
- `GET/POST /workspaces/<slug>/projects/<uuid>/inbox-issues/` - InboxIssueViewSet
- `GET /workspaces/<slug>/projects/<uuid>/inbox-public-issues/` - InboxIssuePublicViewSet (AllowAny)

#### Estimate Endpoints
- `GET /workspaces/<slug>/projects/<uuid>/estimates/<uuid>/points/` - ProjectEstimatePointEndpoint
- `PATCH /workspaces/<slug>/projects/<uuid>/estimates/` - BulkEstimatePointEndpoint

#### Notification Endpoints
- `GET /workspaces/<slug>/notifications/` - NotificationViewSet (list)
- `PATCH /workspaces/<slug>/notifications/<uuid>/` - NotificationViewSet (partial_update)

#### Asset/Upload Endpoints
- `POST /assets/upload/` - FileAssetEndpoint
- `GET /workspaces/<slug>/user-assets/` - UserAssetsEndpoint

#### Integration Endpoints
- `GET /workspaces/<slug>/integrations/` - WorkspaceIntegrationViewSet
- `POST /workspaces/<slug>/projects/<uuid>/github-repositories/` - GithubRepositoriesEndpoint
- `GET/POST /workspaces/<slug>/projects/<uuid>/github-syncs/` - GithubRepositorySyncViewSet
- `GET/POST /workspaces/<slug>/projects/<uuid>/github-issue-syncs/` - GithubIssueSyncViewSet
- `GET/POST /workspaces/<slug>/projects/<uuid>/slack-syncs/` - SlackProjectSyncViewSet

#### Analytics Endpoints
- `GET /workspaces/<slug>/analytics/` - AnalyticsEndpoint
- `POST /workspaces/<slug>/analytics/saved/` - SavedAnalyticEndpoint
- `POST /workspaces/<slug>/analytics/export/` - ExportAnalyticsEndpoint
- `GET /workspaces/<slug>/analytics/default/` - DefaultAnalyticsEndpoint
- `GET/POST /workspaces/<slug>/analytics-views/` - AnalyticViewViewset

#### Import/Export Endpoints
- `GET /workspaces/<slug>/importers/<uuid>/summary/` - ServiceIssueImportSummaryEndpoint
- `POST /workspaces/<slug>/importers/` - ImportServiceEndpoint
- `POST /workspaces/<slug>/importers/<uuid>/` - UpdateServiceImportStatusEndpoint
- `POST /workspaces/<slug>/projects/<uuid>/import-bulk-issues/` - BulkImportIssuesEndpoint
- `POST /workspaces/<slug>/projects/<uuid>/import-bulk-modules/` - BulkImportModulesEndpoint

#### User Endpoints
- `GET /profile/` - UserEndpoint (retrieve current user)
- `GET /profile/preferences/` - UserEndpoint (retrieve_user_settings)
- `PATCH /profile/` - UserEndpoint (partial_update)
- `PATCH /profile/onboard/` - UpdateUserOnBoardedEndpoint
- `PATCH /profile/tour-completed/` - UpdateUserTourCompletedEndpoint
- `GET /workspaces/<slug>/user-activity/` - UserActivityEndpoint
- `GET /workspaces/<slug>/last-project/` - UserLastProjectWithWorkspaceEndpoint

#### Configuration Endpoints
- `GET /config/` - ConfigurationEndpoint

#### External Service Endpoints
- `POST /workspaces/<slug>/ai-assistant/` - GPTIntegrationEndpoint
- `GET /unsplash/` - UnsplashEndpoint (AllowAny)
- `GET /release-notes/` - ReleaseNotesEndpoint (AllowAny)

#### Search Endpoints
- `GET /workspaces/<slug>/search-issues/` - GlobalSearchEndpoint

### 4. PERMISSION CLASSES

**WorkspacePermissions** (`plane/api/permissions/workspace.py`)
- **WorkSpaceBasePermission**: POST allowed for all authenticated; Safe methods allowed; PUT/PATCH for Admin/Owner; DELETE for Owner only
- **WorkSpaceAdminPermission**: Only Owner/Admin
- **WorkspaceEntityPermission**: Read for all members; Write for Admin/Owner
- **WorkspaceViewerPermission**: Read-only for Member+ (role >= 10)

**ProjectPermissions** (`plane/api/permissions/project.py`)
- **ProjectBasePermission**: POST for Admin/Member of workspace; Safe methods for any member; PUT/PATCH/DELETE for project Admin only
- **ProjectMemberPermission**: POST for workspace Admin/Member; Safe/Write for project Admin/Member
- **ProjectEntityPermission**: Read for all project members; Write for Admin/Member
- **ProjectLitePermission**: Checks project member access
- **IssueDraftCreatorPermission**: Only creator can access their drafts

### 5. SERIALIZERS (89 Serializer Classes)

Key Serializers:
- **BaseSerializer**: Model serializer with read_only id
- **DynamicBaseSerializer**: Supports dynamic field filtering via `fields` parameter
- **IssueFlatSerializer**: Minimal fields only
- **IssueCreateSerializer**: Full create/update with nested details
- **IssueSerializer**: Complex read with all relations
- **WorkSpaceSerializer**: With total_members, total_issues counts
- **ProjectSerializer**: With is_favorite, total_issues annotations
- **UserSerializer, UserLiteSerializer, UserAdminLiteSerializer**: Different detail levels
- **CycleSerializer**: With issue counts
- **ModuleSerializer**: With member counts
- **StateSerializer**: With issue counts
- **Integration serializers**: GithubRepositorySyncSerializer, SlackProjectSyncSerializer

### 6. BACKGROUND TASKS (Celery)

**Task Files:**
1. **issue_activites_task.py** - `issue_activity()` task
   - Tracks changes to: name, description, state, priority, estimates, dates, assignees, labels
   - Creates IssueActivity records with old/new values
   - Calls notifications async

2. **notification_task.py** - `notifications()` task
   - Handles @mentions with IssueMention model
   - Extracts mentions from description_html
   - Auto-subscribes mentioned users to issues
   - Filters new/removed mentions

3. **workspace_invitation_task.py** - `workspace_invitation()` task
   - Sends workspace invite emails via SMTP
   - Slack notification integration
   - Renders templates with invitation URLs

4. **project_invitation_task.py** - `project_invitation()` task
   - Similar to workspace invitations

5. **email_verification_task.py** - `email_verification()` task
   - JWT token generation for email verification
   - Email template rendering

6. **magic_link_code_task.py** - `magic_link()` task
   - Generates magic link authentication tokens

7. **forgot_password_task.py** - `forgot_password()` task
   - Password reset email with token

8. **user_welcome_task.py** - `send_welcome_task()` task
   - Welcome email for new users

9. **importer_task.py** - `service_importer()` task
   - Async GitHub/Jira issue imports
   - Bulk issue creation

10. **export_task.py** - `export_issues()` task
    - Async issue export to JSON/CSV/XLSX

11. **exporter_expired_task.py** - `delete_old_exporters()` task
    - Scheduled cleanup of old export files

12. **issue_automation_task.py** - Automation rules execution

13. **analytic_plot_export.py** - Analytics export generation

### 7. AUTHENTICATION FLOW

**Methods:**
1. **Email/Password**: SignUp → SignIn → JWT tokens
2. **OAuth**: Google (id_token verification) and GitHub (code exchange)
3. **Magic Link**: Generate token → Send email → Link verification
4. **JWT Tokens**: simplejwt with 7-day access token, 43200-day refresh token

**Token Generation:**
```python
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return (str(refresh.access_token), str(refresh))
```

**Authentication Header:** `Authorization: Bearer <access_token>`

**Refresh Endpoint:** `POST /auth/token/refresh/` with refresh token

### 8. SETTINGS & CONFIGURATION

**common.py** Key Settings:
- DEBUG: True (default)
- INSTALLED_APPS: 6 plane apps + Django/DRF apps (39 apps total)
- MIDDLEWARE: CORS, Security, Sessions, Auth, GZIP, crum (current user)
- REST_FRAMEWORK:
  - Authentication: JWTAuthentication
  - Permissions: IsAuthenticated (default)
  - Filters: DjangoFilterBackend
  - Renderer: JSONRenderer
- SIMPLE_JWT:
  - ACCESS_TOKEN_LIFETIME: 10080 minutes (7 days)
  - REFRESH_TOKEN_LIFETIME: 43200 days
  - ALGORITHM: HS256
- EMAIL_BACKEND: SMTP
- DATABASE: SQLite default (overridden in production)
- CELERY_TIMEZONE: UTC
- CELERY_TASK_SERIALIZER: JSON
- AUTH_USER_MODEL: db.User
- FILE_SIZE_LIMIT: 5 MB (FileAsset, IssueAttachment)

**Production Settings:**
- Database: PostgreSQL
- Async: Redis (Celery broker)
- File Storage: S3 via django-s3-storage
- Analytics: External analytics API
- Email: SMTP (SendGrid, etc.)
- Sentry: Error tracking

### 9. DATABASE MIGRATIONS (46+ Migration Files)

Key Migrations Track:
- Initial schema creation
- UUID primary keys
- Issue activity tracking
- Workspace themes
- Project deploy boards
- GitHub sync models
- Slack sync models
- Analytics views
- Exporter history
- API tokens
- Archive/close policies
- Page favorites
- Estimate system
- Inbox features

### 10. EXTERNAL INTEGRATIONS

**GitHub** (`plane/utils/integrations/github.py`, `plane/db/models/integration/github.py`)
- OAuth2 authentication
- Repository sync
- Issue sync (two-way)
- Comment sync
- Label mapping
- Models: GithubRepository, GithubRepositorySync, GithubIssueSync, GithubCommentSync

**Slack** (`plane/db/models/integration/slack.py`)
- Webhook integration
- Project sync
- Channel notifications
- Models: SlackProjectSync

**Google OAuth**
- id_token verification via google.oauth2
- Email, first_name, last_name extraction

**GitHub OAuth**
- Code exchange for access token
- User data retrieval
- Repository access

**OpenAI** (external.py)
- GPT integration endpoint
- Query-based issue generation/analysis

**Unsplash** (external.py)
- Image search API integration

**SendGrid/SMTP**
- Email via django.core.mail
- Template rendering

**Sentry**
- Error tracking via sentry-sdk
- Exception capture_exception() calls throughout

**AWS S3**
- File uploads via boto3
- django-s3-storage integration

**Slack Bot**
- User signup notifications
- Invitation tracking
- WebClient from slack-sdk

### 11. UTILITIES & HELPERS

**issue_filters.py** - Dynamic issue filtering by:
- Priority, state, state_group
- Assignees, created_by, labels
- Start/target dates, subscribers

**issue_search.py** - Full-text search on:
- Issue name, description_stripped
- Comments

**grouper.py** - Result grouping by:
- State, assignees, priority, labels
- Created by, created on, due date

**html_processor.py** - strip_tags() utility for cleaning HTML

**paginator.py** - BasePaginator with configurable page size

**analytics_plot.py** - Chart data generation

**markdown.py** - Markdown to HTML conversion

### 12. MANAGEMENT COMMANDS

**wait_for_db.py** - Health check on startup (waits for database connection)

### 13. KEY DEPENDENCIES

Core:
- Django==4.2.5
- djangorestframework==3.14.0
- django-filter==23.2
- djangorestframework-simplejwt==5.3.0

Real-time & Async:
- celery==5.3.4
- django_celery_beat==2.5.0
- channels==4.0.0
- redis==4.6.0

Database:
- psycopg==3.1.10 (PostgreSQL)

OAuth/Auth:
- google-auth==2.22.0
- django-allauth==0.55.2
- dj_rest_auth==2.2.5

Integration:
- slack-sdk==3.21.3
- openai==0.28.0
- google-api-python-client==2.97.0

File Storage:
- django-s3-storage==0.14.0
- openpyxl==3.1.2 (Excel export)

Utilities:
- beautifulsoup4==4.12.2 (HTML parsing)
- sentry-sdk==1.30.0
- django-crum==0.7.9 (Current request user)
- django-cors-headers==4.2.0

Deployment:
- uvicorn==0.23.2 (ASGI server)
- whitenoise==6.5.0 (Static files)
- gunicorn (WSGI server)

### 14. KEY ARCHITECTURAL PATTERNS

**BaseModel Pattern:**
- All models inherit from BaseModel → AuditModel → Django Model
- UUID primary key
- Automatic created_by/updated_by tracking via crum middleware
- created_at/updated_at timestamps

**Permission Layering:**
1. Workspace level: Owner/Admin/Member/Guest hierarchy
2. Project level: Admin/Member/Viewer/Guest hierarchy
3. Resource level: ViewSets check permissions on read/write

**Serializer Pattern:**
- Model-based with custom fields
- Nested relations with *Serializer(read_only=True)
- List vs. Detail serializers via get_serializer_class()

**View Pattern:**
- BaseViewSet for CRUD with defaults
- BaseAPIView for custom endpoints
- Error handling via handle_exception()
- Timezone activation per user
- Pagination via BasePaginator

**Async Task Pattern:**
- Celery @shared_task decorator
- Delay execution with `.delay()`
- Email, notifications, imports/exports queued
- Signal handlers trigger tasks (post_save)

**Filtering Pattern:**
- issue_filters.py for complex query building
- DjangoFilterBackend for simple filtering
- SearchFilter for text search
- Custom get_queryset() in ViewSets

### 15. CRITICAL FLOW EXAMPLES

**Issue Creation Flow:**
1. POST /workspaces/<slug>/projects/<uuid>/issues/
2. IssueCreateSerializer validates data
3. IssueViewSet.create() calls perform_create()
4. Issue.save() auto-assigns default state, sequence_id, sort_order
5. Signal triggers issue_activity task
6. Activity task creates IssueActivity record
7. Notification task sends to subscribers

**Invitation Flow:**
1. POST /workspaces/<slug>/invite/
2. InviteWorkspaceEndpoint creates WorkspaceMemberInvite
3. workspace_invitation async task sent to Celery
4. Task renders email template
5. SMTP sends email with invitation token/URL
6. Invitee clicks link, accepts invitation
7. WorkspaceMember record created

**GitHub Sync Flow:**
1. User authenticates GitHub via OAuth
2. GithubRepositorySync created with credentials
3. Repositories fetched via GitHub API
4. User selects repositories to sync
5. GithubIssueSync records created for mapped issues
6. Webhook or scheduled task syncs comments/updates
7. IssueActivity created for sync activities

---

## SUMMARY

This is a sophisticated Django/DRF backend API for a project management platform with:
- **Multi-tenant** workspace architecture
- **Complex permissions** with role-based access control
- **Real-time collaboration** via WebSockets (Channels) + Redis
- **Async processing** for email, imports, exports, analytics
- **Rich integrations** with GitHub, Slack, Google, OpenAI
- **Comprehensive audit trail** of all changes
- **Advanced issue filtering** and search
- **Customizable views** and analytics

The codebase follows Django best practices with clear separation of concerns: models → views → serializers → permissions → URLs, with business logic delegated to Celery tasks.

**Key Files to Start With:**
1. `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/plane/db/models/__init__.py` - Model registry
2. `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/plane/api/urls/__init__.py` - Complete URL routing
3. `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/plane/api/views/base.py` - Base request/response handling
4. `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/plane/settings/common.py` - Django configuration

---

