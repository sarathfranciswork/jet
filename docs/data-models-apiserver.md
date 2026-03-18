# Data Models - API Server

**Generated:** 2026-03-18
**Database:** PostgreSQL 15.2
**ORM:** Django 4.2.5

## Base Model Pattern

All models inherit from `BaseModel` which provides:
- `id` — UUID primary key (auto-generated)
- `created_at` — DateTime (auto)
- `updated_at` — DateTime (auto)
- `created_by` — ForeignKey to User (via `crum` middleware, auto-captured)
- `updated_by` — ForeignKey to User (via `crum` middleware, auto-captured)

---

## Core Models

### User (`plane.db.models.user`)
Custom user model extending `AbstractBaseUser` + `PermissionsMixin`.

| Field | Type | Notes |
|-------|------|-------|
| id | UUID | Primary key |
| email | CharField | Unique |
| username | CharField | Unique |
| mobile_number | CharField | Optional |
| first_name | CharField | |
| last_name | CharField | |
| display_name | CharField | max 255 |
| avatar | CharField | URL |
| cover_image | URLField | Optional |
| is_active | Boolean | Default true |
| is_superuser | Boolean | |
| is_staff | Boolean | |
| is_email_verified | Boolean | Default false |
| is_onboarded | Boolean | Default false |
| is_tour_completed | Boolean | Default false |
| is_bot | Boolean | Default false |
| token | CharField | Auth token |
| billing_address_country | CharField | |
| billing_address | JSONField | |
| user_timezone | CharField | Default UTC |
| last_active | DateTimeField | |
| last_login_time | DateTimeField | |
| last_login_ip | CharField | |
| last_login_medium | CharField | |
| last_login_uagent | TextField | |
| last_workspace_id | UUIDField | |
| my_issues_prop | JSONField | Saved issue preferences |
| role | CharField | Optional |
| onboarding_step | JSONField | Tracks onboarding progress |
| theme | JSONField | UI theme preferences |

**Signal:** Sends Slack notification on user creation.

---

### Workspace (`plane.db.models.workspace`)

| Field | Type | Notes |
|-------|------|-------|
| name | CharField | max 80 |
| logo | URLField | Optional |
| slug | SlugField | Unique, max 48 |
| owner | FK → User | |
| organization_size | CharField | Optional |

**Related Models:**

#### WorkspaceMember
| Field | Type | Notes |
|-------|------|-------|
| workspace | FK → Workspace | |
| member | FK → User | |
| role | SmallInt | Owner=20, Admin=15, Member=10, Guest=5 |
| company_role | TextField | Optional |
| view_props | JSONField | Saved view preferences |
| default_props | JSONField | Default filter/display settings |
| issue_props | JSONField | Issue display preferences |
| **Unique:** | workspace + member | |

#### WorkspaceMemberInvite
| Field | Type | Notes |
|-------|------|-------|
| workspace | FK → Workspace | |
| email | CharField | |
| accepted | Boolean | Default false |
| token | CharField | Max 255 |
| message | TextField | Optional |
| responded_at | DateTimeField | Optional |
| role | SmallInt | Default Member=10 |
| **Unique:** | email + workspace | |

#### Team
| Field | Type | Notes |
|-------|------|-------|
| name | CharField | |
| description | TextField | Optional |
| workspace | FK → Workspace | |
| members | M2M → User | Through TeamMember |
| **Unique:** | name + workspace | |

#### WorkspaceTheme
| Field | Type | Notes |
|-------|------|-------|
| workspace | FK → Workspace | |
| actor | FK → User | |
| name | CharField | Max 300 |
| colors | JSONField | Theme color definitions |

---

### Project (`plane.db.models.project`)

| Field | Type | Notes |
|-------|------|-------|
| name | CharField | Max 255 |
| description | TextField | Optional |
| description_text | JSONField | Optional |
| description_html | JSONField | Optional |
| identifier | CharField | Max 12 (e.g., "PROJ") |
| workspace | FK → Workspace | |
| network | SmallInt | 0=Secret, 2=Public |
| emoji | CharField | Optional |
| icon_prop | JSONField | Optional |
| module_view | Boolean | Default true |
| cycle_view | Boolean | Default true |
| issue_views_view | Boolean | Default true |
| page_view | Boolean | Default true |
| inbox_view | Boolean | Default false |
| cover_image | URLField | Optional |
| estimate | FK → Estimate | Optional |
| archive_in | IntegerField | Months (0=disabled, 1-12) |
| close_in | IntegerField | Months (0=disabled, 1-12) |
| default_assignee | FK → User | Optional |
| project_lead | FK → User | Optional |
| default_state | FK → State | Optional |
| sort_order | FloatField | Default 65535 |

#### ProjectMember
| Field | Type | Notes |
|-------|------|-------|
| project | FK → Project | |
| member | FK → User | |
| role | SmallInt | Admin=20, Member=15, Viewer=10, Guest=5 |
| view_props | JSONField | |
| default_props | JSONField | |
| preferences | JSONField | |
| sort_order | FloatField | |
| **Unique:** | project + member | |

#### ProjectIdentifier
| Field | Type | Notes |
|-------|------|-------|
| project | OneToOne → Project | |
| workspace | FK → Workspace | |
| name | CharField | Max 12 |
| **Unique:** | name + workspace | |

#### ProjectFavorite
| Field | Type | Notes |
|-------|------|-------|
| project | FK → Project | |
| user | FK → User | |
| workspace | FK → Workspace | |
| **Unique:** | project + user | |

#### ProjectDeployBoard
| Field | Type | Notes |
|-------|------|-------|
| project | FK → Project | |
| workspace | FK → Workspace | |
| anchor | CharField | Unique deploy anchor |
| comments | Boolean | |
| reactions | Boolean | |
| inbox | FK → Inbox | Optional |
| votes | Boolean | |
| views | JSONField | Enabled board views |

---

### Issue (`plane.db.models.issue`)

| Field | Type | Notes |
|-------|------|-------|
| name | CharField | Max 255 |
| description | JSONField | Rich text (TipTap JSON) |
| description_html | TextField | HTML representation |
| description_stripped | TextField | Plain text |
| priority | CharField | urgent/high/medium/low/none |
| state | FK → State | |
| project | FK → Project | |
| workspace | FK → Workspace | |
| parent | FK → self | Sub-issue support |
| assignees | M2M → User | Through IssueAssignee |
| labels | M2M → Label | Through IssueLabel |
| estimate_point | IntegerField | Optional (story points) |
| start_date | DateField | Optional |
| target_date | DateField | Optional |
| completed_at | DateTimeField | Optional |
| archived_at | DateTimeField | Optional |
| is_draft | Boolean | Default false |
| sequence_id | IntegerField | Auto-incremented per project |
| sort_order | FloatField | Default 65535 |

**Custom Manager:** `issue_objects` filters out archived and draft issues by default.

#### IssueActivity
| Field | Type | Notes |
|-------|------|-------|
| issue | FK → Issue | |
| verb | CharField | created/updated |
| field | CharField | Changed field name |
| old_value | TextField | Previous value |
| new_value | TextField | New value |
| old_identifier | UUIDField | Optional |
| new_identifier | UUIDField | Optional |
| actor | FK → User | |
| issue_comment | FK → IssueComment | Optional |
| epoch | FloatField | Timestamp for grouping |

#### IssueComment
| Field | Type | Notes |
|-------|------|-------|
| comment_stripped | TextField | |
| comment_json | JSONField | |
| comment_html | TextField | |
| issue | FK → Issue | |
| actor | FK → User | |
| attachments | ArrayField | URLs |
| access | CharField | INTERNAL/EXTERNAL |

#### IssueAssignee
| Field | Type | Notes |
|-------|------|-------|
| issue | FK → Issue | |
| assignee | FK → User | |
| **Unique:** | issue + assignee | |

#### IssueLabel
| Field | Type | Notes |
|-------|------|-------|
| issue | FK → Issue | |
| label | FK → Label | |
| **Unique:** | issue + label | |

#### Label
| Field | Type | Notes |
|-------|------|-------|
| name | CharField | |
| description | TextField | Optional |
| color | CharField | Hex color, default #c0c0c0 |
| project | FK → Project | |
| workspace | FK → Workspace | |
| parent | FK → self | Label groups |
| sort_order | FloatField | |

#### IssueLink
| Field | Type | Notes |
|-------|------|-------|
| title | CharField | Optional |
| url | URLField | Max 255 |
| issue | FK → Issue | |

#### IssueAttachment
| Field | Type | Notes |
|-------|------|-------|
| attributes | JSONField | Metadata |
| asset | FileField | S3 upload |
| issue | FK → Issue | |

#### IssueReaction
| Field | Type | Notes |
|-------|------|-------|
| actor | FK → User | |
| issue | FK → Issue | |
| reaction | CharField | Emoji |
| **Unique:** | actor + issue + reaction | |

#### CommentReaction
| Field | Type | Notes |
|-------|------|-------|
| actor | FK → User | |
| comment | FK → IssueComment | |
| reaction | CharField | Emoji |
| **Unique:** | actor + comment + reaction | |

#### IssueSubscriber
| Field | Type | Notes |
|-------|------|-------|
| subscriber | FK → User | |
| issue | FK → Issue | |
| **Unique:** | subscriber + issue | |

#### IssueRelation
| Field | Type | Notes |
|-------|------|-------|
| issue | FK → Issue | |
| related_issue | FK → Issue | |
| relation_type | CharField | blocked_by/duplicate/relates_to |
| **Unique:** | issue + related_issue | |

#### IssueVote
| Field | Type | Notes |
|-------|------|-------|
| issue | FK → Issue | |
| actor | FK → User | |
| vote | IntegerField | 1=upvote, -1=downvote |
| **Unique:** | issue + actor | |

---

### State (`plane.db.models.state`)

| Field | Type | Notes |
|-------|------|-------|
| name | CharField | Max 100 |
| description | TextField | Optional |
| color | CharField | Hex color |
| slug | SlugField | Auto from name |
| project | FK → Project | |
| workspace | FK → Workspace | |
| group | CharField | backlog/unstarted/started/completed/cancelled |
| default | Boolean | |
| sequence | FloatField | Ordering |
| **Unique:** | name + project | |

---

### Cycle (`plane.db.models.cycle`)

| Field | Type | Notes |
|-------|------|-------|
| name | CharField | Max 255 |
| description | TextField | Optional |
| start_date | DateField | Optional |
| end_date | DateField | Optional |
| owned_by | FK → User | |
| project | FK → Project | |
| workspace | FK → Workspace | |
| view_props | JSONField | Default {} |
| sort_order | FloatField | Auto-calculated |

#### CycleIssue
| Field | Type | Notes |
|-------|------|-------|
| issue | OneToOne → Issue | Each issue in max 1 cycle |
| cycle | FK → Cycle | |

#### CycleFavorite
| Field | Type | Notes |
|-------|------|-------|
| cycle | FK → Cycle | |
| user | FK → User | |
| **Unique:** | cycle + user | |

---

### Module (`plane.db.models.module`)

| Field | Type | Notes |
|-------|------|-------|
| name | CharField | Max 255 |
| description | TextField | Optional |
| description_text | JSONField | Optional |
| description_html | JSONField | Optional |
| status | CharField | backlog/planned/in-progress/paused/completed/cancelled |
| lead | FK → User | Optional |
| members | M2M → User | Through ModuleMember |
| start_date | DateField | Optional |
| target_date | DateField | Optional |
| project | FK → Project | |
| workspace | FK → Workspace | |
| sort_order | FloatField | |

#### ModuleIssue
| Field | Type | Notes |
|-------|------|-------|
| module | FK → Module | |
| issue | FK → Issue | |
| **Unique:** | issue + module | |

#### ModuleLink
| Field | Type | Notes |
|-------|------|-------|
| title | CharField | Optional |
| url | URLField | Max 255 |
| module | FK → Module | |

#### ModuleFavorite, ModuleMember
Standard through/favorite models.

---

### Page (`plane.db.models.page`)

| Field | Type | Notes |
|-------|------|-------|
| name | CharField | Max 255 |
| description | JSONField | Rich text |
| description_html | TextField | Optional |
| description_stripped | TextField | Optional |
| owned_by | FK → User | |
| access | SmallInt | 0=Public, 1=Private |
| color | CharField | Optional |
| project | FK → Project | |
| workspace | FK → Workspace | |
| labels | M2M → Label | Through PageLabel |

#### PageBlock
| Field | Type | Notes |
|-------|------|-------|
| page | FK → Page | |
| name | CharField | Max 255 |
| description | JSONField | |
| description_html | TextField | Optional |
| description_stripped | TextField | Optional |
| issue | FK → Issue | Optional (sync to issue) |
| completed_at | DateTimeField | Optional |
| sort_order | FloatField | |
| sync | Boolean | Default true |

---

### Inbox (`plane.db.models.inbox`)

| Field | Type | Notes |
|-------|------|-------|
| name | CharField | Max 255 |
| description | TextField | Optional |
| is_default | Boolean | Default true |
| view_props | JSONField | |
| project | FK → Project | |
| workspace | FK → Workspace | |
| **Unique:** | name + project | |

#### InboxIssue
| Field | Type | Notes |
|-------|------|-------|
| inbox | FK → Inbox | |
| issue | FK → Issue | |
| status | IntegerField | -2=Pending, -1=Rejected, 0=Snoozed, 1=Accepted, 2=Duplicate |
| snoozed_till | DateTimeField | Optional |
| duplicate_to | FK → Issue | Optional |
| source | CharField | Optional |

---

### Estimate (`plane.db.models.estimate`)

| Field | Type | Notes |
|-------|------|-------|
| name | CharField | Max 255 |
| description | TextField | Optional |
| project | FK → Project | |
| workspace | FK → Workspace | |
| **Unique:** | name + project | |

#### EstimatePoint
| Field | Type | Notes |
|-------|------|-------|
| estimate | FK → Estimate | |
| key | IntegerField | 0-7 |
| description | TextField | Optional |
| value | CharField | Max 20 |

---

### Notification (`plane.db.models.notification`)

| Field | Type | Notes |
|-------|------|-------|
| workspace | FK → Workspace | |
| project | FK → Project | Optional |
| title | CharField | |
| message | JSONField | Optional |
| data | JSONField | Optional |
| entity_identifier | UUIDField | Optional |
| entity_name | CharField | |
| sender | CharField | |
| triggered_by | FK → User | |
| receiver | FK → User | |
| read_at | DateTimeField | Optional |
| snoozed_till | DateTimeField | Optional |
| archived_at | DateTimeField | Optional |

---

### APIToken (`plane.db.models.api_token`)

| Field | Type | Notes |
|-------|------|-------|
| token | CharField | Unique, auto-generated |
| label | CharField | Max 255, auto-generated |
| user | FK → User | |
| user_type | SmallInt | 0=Human, 1=Bot |
| workspace | FK → Workspace | Optional |

---

### FileAsset (`plane.db.models.asset`)

| Field | Type | Notes |
|-------|------|-------|
| attributes | JSONField | Metadata |
| asset | FileField | S3 upload path |
| workspace | FK → Workspace | Optional |

**Validator:** Max file size configurable (default 5MB).

---

### Integration Models

#### GithubRepository
| Field | Type | Notes |
|-------|------|-------|
| name | CharField | |
| url | URLField | Optional |
| config | JSONField | |
| repository_id | BigIntegerField | |
| owner | CharField | |
| project_id | UUIDField | |

#### GithubRepositorySync
| Field | Type | Notes |
|-------|------|-------|
| repository | OneToOne → GithubRepository | |
| workspace_integration | FK → WorkspaceIntegration | |
| actor | FK → User | |
| credentials | JSONField | |
| label | FK → Label | Optional |

#### GithubIssueSync
| Field | Type | Notes |
|-------|------|-------|
| repo_issue_id | BigIntegerField | |
| github_issue_id | BigIntegerField | |
| issue_url | TextField | |
| issue | FK → Issue | |
| repository_sync | FK → GithubRepositorySync | |
| **Unique:** | repository_sync + issue | |

#### SlackProjectSync
| Field | Type | Notes |
|-------|------|-------|
| access_token | CharField | |
| scopes | TextField | |
| bot_user_id | CharField | |
| webhook_url | URLField | |
| data | JSONField | |
| team_id | CharField | |
| team_name | CharField | |
| workspace_integration | FK → WorkspaceIntegration | |
| project | FK → Project | |
| **Unique:** | team_id + project | |

---

### Importer (`plane.db.models.importer`)

| Field | Type | Notes |
|-------|------|-------|
| project | FK → Project | |
| workspace | FK → Workspace | |
| service | CharField | github/jira |
| status | CharField | queued/processing/completed/failed |
| initiated_by | FK → User | |
| metadata | JSONField | |
| config | JSONField | |
| data | JSONField | |
| token | FK → APIToken | |
| imported_data | JSONField | Optional |

### ExporterHistory (`plane.db.models.exporter`)

| Field | Type | Notes |
|-------|------|-------|
| workspace | FK → Workspace | |
| project | ArrayField(UUID) | |
| provider | CharField | json/csv/xlsx |
| status | CharField | queued/processing/completed/failed |
| reason | TextField | Optional |
| key | CharField | Storage path |
| url | URLField | Download URL |
| token | CharField | |
| initiated_by | FK → User | |

### AnalyticView (`plane.db.models.analytic`)

| Field | Type | Notes |
|-------|------|-------|
| workspace | FK → Workspace | |
| name | CharField | Max 255 |
| description | TextField | Optional |
| query | JSONField | |
| query_dict | JSONField | |

---

## Entity Relationship Summary

```
User ──┬── WorkspaceMember ──── Workspace
       ├── ProjectMember ────── Project ──── Workspace
       ├── IssueAssignee ────── Issue ────── Project
       └── Notification ─────── Workspace/Project

Workspace ──┬── Project ──┬── Issue ──┬── IssueComment
            │             │           ├── IssueActivity
            │             │           ├── IssueAttachment
            │             │           ├── IssueReaction
            │             │           ├── IssueRelation
            │             │           └── IssueSubscriber
            │             ├── State
            │             ├── Label
            │             ├── Cycle ──── CycleIssue
            │             ├── Module ── ModuleIssue
            │             ├── Page ──── PageBlock
            │             ├── View
            │             ├── Inbox ─── InboxIssue
            │             └── Estimate ─ EstimatePoint
            ├── Team
            └── WorkspaceTheme

Issue (self-referencing via parent FK for sub-issues)
Issue ← IssueVote (for public boards)
Issue ← CycleIssue (OneToOne - issue in max 1 cycle)
Issue ← ModuleIssue (issue can be in multiple modules)
```

## Migration History

46+ migration files tracking schema evolution including:
- Initial schema with UUID primary keys
- Issue activity tracking system
- Workspace themes and customization
- Project deploy boards (public sharing)
- GitHub and Slack sync models
- Analytics views
- Export history
- API tokens for bot/service auth
- Archive/close automation policies
- Page favorites
- Estimate system (story points)
- Inbox feature
- Issue relations and votes
