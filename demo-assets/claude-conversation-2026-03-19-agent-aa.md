# Claude Conversation Log

Session ID: agent-aae1dd876bcf5f6da
Date: 2026-03-19 02:01:05

---

## 👤 User

You are designing the implementation plan for adding full GitHub integration (like Plane Pro) to the Jet project management tool.

## CURRENT STATE

The codebase already has a PARTIAL GitHub integration:

### What EXISTS:
1. **Models** (all exist in `apiserver/jet/db/models/integration/`):
   - Integration, WorkspaceIntegration (base)
   - GithubRepository, GithubRepositorySync, GithubIssueSync, GithubCommentSync

2. **GitHub App auth** (`apiserver/jet/utils/integrations/github.py`):
   - JWT token generation from GITHUB_APP_ID + GITHUB_APP_PRIVATE_KEY
   - Installation metadata fetching
   - Repository listing
   - App installation/deletion

3. **Import flow** (backend + frontend):
   - Multi-step import wizard (5 steps: configure, data, repo details, users, confirm)
   - Service importer Celery task
   - User mapping/invitation
   - Bulk issue creation

4. **Frontend components** (`web/components/integration/github/`):
   - GithubImporterRoot, auth, import-configure, import-data, repo-details, import-users, import-confirm, select-repository

5. **API endpoints**: Integration CRUD, workspace integration, GitHub repo listing, repo sync, issue sync, comment sync

### What's MISSING (needs to be built):

1. **Webhook handler endpoint** — No active endpoint to receive GitHub webhook events (push, issue, PR, comment events). The infrastructure (webhook_url, webhook_secret fields) exists in the Integration model but no handler view.

2. **Bidirectional sync engine** — Models exist but actual sync logic is delegated to an external PROXY_BASE_URL service that doesn't exist in self-hosted. Need to build the sync engine natively.

3. **PR automation** — No PR-related models or logic:
   - No PR state mapping (draft→started, merged→completed, etc.)
   - No PR-to-issue linking via [WEB-344] reference parsing
   - No PR model to track linked PRs

4. **Label-based sync triggers** — Adding "GitHub" label to Jet issue should create GitHub issue; adding configured label to GitHub issue should create Jet issue

5. **State mapping** — No UI or backend for mapping GitHub open/closed states to Jet workflow states

6. **Comment bidirectional sync** — GithubCommentSync model exists but no sync logic

7. **Real-time sync** — Only manual import trigger exists, no webhook-driven real-time updates

## TARGET STATE (from Plane Pro docs)

The full integration should support:

### Core Sync Features:
- Bidirectional sync of: title, description, assignees, labels, states, comments, mentions
- Unidirectional option (GitHub → Jet only)
- Label-based triggers ("Jet" label on GitHub issue creates Jet issue, "GitHub" label on Jet issue creates GitHub issue)
- Issue link references displayed with direct links

### PR Automation:
- Map PR lifecycle states to Jet issue states:
  - Draft PR created → configurable state
  - PR opened → configurable state
  - Review requested → configurable state
  - Approved → configurable state
  - Merged → configurable state
  - Closed without merge → configurable state
- Reference format: [WEB-344] in PR title/body triggers state automation
- WEB-344 without brackets links as reference only (no automation)

### Configuration:
- Project-level sync mapping (Jet project ↔ GitHub repo)
- State mapping (GitHub open/closed ↔ Jet states)
- Sync direction selection (bidirectional vs unidirectional)
- PR automation state mapping
- Personal GitHub account connection for comment attribution

## TECHNICAL CONSTRAINTS

- **Stack**: Django 4.2.5 + DRF (backend), Next.js 12.3.2 + React 18 + MobX (frontend)
- **Async**: Celery for background tasks
- **Auth**: GitHub App with JWT (already implemented)
- **Database**: PostgreSQL with Django ORM
- **Existing patterns**: Bot user pattern, API token pattern, label-based grouping

## DESIGN REQUIREMENTS

Please design:

1. **New models needed** (with fields)
2. **New API endpoints** (with methods, permissions)
3. **Webhook handler architecture** (events to handle, processing flow)
4. **Sync engine design** (how bidirectional sync works, conflict resolution)
5. **PR automation design** (reference parsing, state mapping)
6. **Frontend components needed** (new pages, settings UI)
7. **Migration strategy** (how to add without breaking existing import flow)
8. **Testing approach**

Organize into implementable epics and stories (like the rebrand planning).

Be specific about file paths, function signatures, and model fields. Reference existing code that should be reused.

---

## 🤖 Claude



I'll start by thoroughly exploring the codebase to understand the existing patterns, models, and architecture before designing the implementation plan.

---

## 🤖 Claude

Now let me read the existing integration models, views, serializers, and utils.

---

## 🤖 Claude

Now let me explore the core models (Issue, State, Label, IssueComment, IssueActivity, etc.) and the base model patterns.

---

## 🤖 Claude

Now let me look at the existing project settings pages, the celery configuration, the URL routing structure, and some key frontend patterns.

---

## 🤖 Claude

Now let me look at the frontend project settings pages structure, the issue activity task (used as a pattern for sync events), and the existing integration frontend components.

---

## 🤖 Claude

Let me now look at the frontend types, existing stores, and GitHub frontend components.

---

## 🤖 Claude

Let me check some more patterns - the types for integration and the model __init__ and existing permissions.

---

## 🤖 Claude

Now let me check the permissions module and the BaseViewSet/BaseAPIView pattern.

---

## 🤖 Claude

Let me check the remaining settings and the existing migration files pattern.

---

## 🤖 Claude

Let me check the existing project integration card component and examine the main URL routing.

---

## 🤖 Claude

Let me also check the env configuration and the PROXY_BASE_URL usage.

---

## 🤖 Claude

Let me check the issue activities task's PROXY_BASE_URL usage more closely to understand the external sync pattern, and the project service in the frontend.

---

## 🤖 Claude

Now let me check the existing tests pattern.

---

## 🤖 Claude

I now have a comprehensive understanding of the codebase. Let me review a few more frontend details - the store root and the constant fetch keys.

---

## 🤖 Claude

I now have a thorough understanding of the full codebase. Let me compile the comprehensive implementation plan.

---

# Full GitHub Integration Implementation Plan for Jet

## Executive Summary

This plan adds complete bidirectional GitHub integration to Jet, replacing the current import-only flow and external PROXY_BASE_URL dependency with a native sync engine. The implementation is organized into 8 epics, ordered by dependency chain, with approximately 35 stories total.

---

## 1. NEW MODELS

All new models go in `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/db/models/integration/github.py`, appending to the existing file. A new migration file (e.g., `0048_github_full_integration.py`) covers all schema changes.

### 1a. GithubSyncConfig (new model)

Project-level configuration for a GitHub sync (extends the existing GithubRepositorySync which is too limited).

```python
class GithubSyncConfig(ProjectBaseModel):
    SYNC_DIRECTION_CHOICES = (
        ("bidirectional", "Bidirectional"),
        ("github_to_jet", "GitHub to Jet"),
    )
    
    repository_sync = models.OneToOneField(
        "db.GithubRepositorySync", on_delete=models.CASCADE, related_name="sync_config"
    )
    sync_direction = models.CharField(
        max_length=20, choices=SYNC_DIRECTION_CHOICES, default="bidirectional"
    )
    # Label on Jet that triggers GitHub issue creation
    jet_trigger_label = models.ForeignKey(
        "db.Label", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="github_jet_trigger_configs"
    )
    # Label name on GitHub that triggers Jet issue creation (e.g., "Jet")
    github_trigger_label = models.CharField(max_length=255, default="Jet")
    
    # State mappings stored as JSON: {"open": "<jet_state_uuid>", "closed": "<jet_state_uuid>"}
    state_mapping = models.JSONField(default=dict)
    
    # PR automation state mappings: {"draft": "<uuid>", "open": "<uuid>", "review_requested": "<uuid>", ...}
    pr_state_mapping = models.JSONField(default=dict)
    
    # Whether to sync comments
    sync_comments = models.BooleanField(default=True)
    # Whether to sync labels  
    sync_labels = models.BooleanField(default=True)
    # Whether to sync assignees
    sync_assignees = models.BooleanField(default=True)
    
    # Webhook tracking
    webhook_id = models.BigIntegerField(null=True, blank=True)
    webhook_secret = models.CharField(max_length=255, blank=True)
    
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "github_sync_configs"
        ordering = ("-created_at",)
```

### 1b. GithubPullRequest (new model)

Tracks linked pull requests.

```python
class GithubPullRequest(ProjectBaseModel):
    PR_STATE_CHOICES = (
        ("draft", "Draft"),
        ("open", "Open"),
        ("review_requested", "Review Requested"),
        ("approved", "Approved"),
        ("merged", "Merged"),
        ("closed", "Closed"),
    )
    
    pr_number = models.IntegerField()
    github_pr_id = models.BigIntegerField()
    title = models.CharField(max_length=1024)
    url = models.URLField()
    state = models.CharField(max_length=20, choices=PR_STATE_CHOICES, default="open")
    is_draft = models.BooleanField(default=False)
    
    # Can be null if PR only references issue as link, not automation
    issue = models.ForeignKey(
        "db.Issue", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="github_prs"
    )
    repository_sync = models.ForeignKey(
        "db.GithubRepositorySync", on_delete=models.CASCADE, related_name="pull_requests"
    )
    
    # Whether this PR triggers state automation (bracket reference [WEB-123])
    # vs just being a link reference (bare WEB-123)
    triggers_automation = models.BooleanField(default=False)
    
    author_login = models.CharField(max_length=255, blank=True)
    author_avatar_url = models.URLField(blank=True, null=True)
    
    merged_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ["repository_sync", "pr_number"]
        db_table = "github_pull_requests"
        ordering = ("-created_at",)
```

### 1c. GithubUserMapping (new model)

Maps GitHub users to Jet users for comment attribution and assignee sync.

```python
class GithubUserMapping(BaseModel):
    workspace = models.ForeignKey(
        "db.Workspace", on_delete=models.CASCADE, related_name="github_user_mappings"
    )
    user = models.ForeignKey(
        "db.User", on_delete=models.CASCADE, related_name="github_mappings"
    )
    github_user_id = models.BigIntegerField()
    github_username = models.CharField(max_length=255)
    github_access_token = models.CharField(max_length=255, blank=True)  # Personal token for comment attribution

    class Meta:
        unique_together = ["workspace", "github_user_id"]
        db_table = "github_user_mappings"
        ordering = ("-created_at",)
```

### 1d. GithubSyncLog (new model)

Audit trail for sync events.

```python
class GithubSyncLog(ProjectBaseModel):
    SYNC_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("success", "Success"),
        ("failed", "Failed"),
    )
    ENTITY_CHOICES = (
        ("issue", "Issue"),
        ("comment", "Comment"),
        ("pull_request", "Pull Request"),
        ("label", "Label"),
        ("state", "State"),
    )
    DIRECTION_CHOICES = (
        ("github_to_jet", "GitHub to Jet"),
        ("jet_to_github", "Jet to GitHub"),
    )
    
    repository_sync = models.ForeignKey(
        "db.GithubRepositorySync", on_delete=models.CASCADE, related_name="sync_logs"
    )
    entity_type = models.CharField(max_length=20, choices=ENTITY_CHOICES)
    entity_id = models.CharField(max_length=255)  # UUID or GitHub ID
    direction = models.CharField(max_length=20, choices=DIRECTION_CHOICES)
    status = models.CharField(max_length=20, choices=SYNC_STATUS_CHOICES, default="pending")
    error_message = models.TextField(blank=True)
    webhook_event_id = models.CharField(max_length=255, blank=True)  # GitHub delivery ID
    payload = models.JSONField(default=dict)  # Sanitized payload for debugging

    class Meta:
        db_table = "github_sync_logs"
        ordering = ("-created_at",)
```

### 1e. Modifications to Existing Models

**GithubIssueSync** -- add fields:
- `github_issue_number = models.IntegerField(null=True)` (the human-readable #123 number)
- `last_synced_at = models.DateTimeField(null=True)` (for conflict resolution)
- `sync_direction = models.CharField(max_length=20, default="bidirectional")`

**GithubCommentSync** -- add fields:
- `github_comment_id = models.BigIntegerField(null=True)` (to distinguish from repo_comment_id if needed)  
- `last_synced_at = models.DateTimeField(null=True)`

---

## 2. NEW API ENDPOINTS

### 2a. Webhook Handler (Unauthenticated, HMAC-verified)

**File**: New file `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/api/views/integration/github_webhook.py`

```
POST /api/webhooks/github/                         # Main webhook receiver
```

This endpoint must:
- Be exempt from CSRF and JWT authentication
- Validate the `X-Hub-Signature-256` header using the webhook secret stored in GithubSyncConfig
- Route by `X-GitHub-Event` header to handler functions
- Return 200 immediately, enqueue Celery task for actual processing

**Permission**: Custom `GithubWebhookPermission` that validates HMAC signature.

### 2b. Sync Configuration Endpoints

**File**: Extend `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/api/views/integration/github.py`

```
GET/POST     /api/workspaces/<slug>/projects/<project_id>/github-sync-config/
GET/PATCH    /api/workspaces/<slug>/projects/<project_id>/github-sync-config/<pk>/
POST         /api/workspaces/<slug>/projects/<project_id>/github-sync-config/<pk>/activate/
POST         /api/workspaces/<slug>/projects/<project_id>/github-sync-config/<pk>/deactivate/
```

**Permission**: `ProjectBasePermission` (Admin for write, Member for read).

### 2c. PR Endpoints

```
GET          /api/workspaces/<slug>/projects/<project_id>/github-pull-requests/
GET          /api/workspaces/<slug>/projects/<project_id>/issues/<issue_id>/github-pull-requests/
```

**Permission**: `ProjectEntityPermission`

### 2d. User Mapping Endpoints

```
GET/POST     /api/workspaces/<slug>/github-user-mappings/
DELETE       /api/workspaces/<slug>/github-user-mappings/<pk>/
POST         /api/workspaces/<slug>/github-user-mappings/connect/     # OAuth flow for personal token
```

**Permission**: `WorkSpaceAdminPermission` for list; individual users can manage their own.

### 2e. Sync Log Endpoints

```
GET          /api/workspaces/<slug>/projects/<project_id>/github-sync-logs/
GET          /api/workspaces/<slug>/projects/<project_id>/github-sync-logs/<pk>/
```

**Permission**: `ProjectBasePermission`

### 2f. Manual Sync Trigger

```
POST         /api/workspaces/<slug>/projects/<project_id>/github-sync-config/<pk>/trigger-sync/
```

**Permission**: `ProjectBasePermission` (Admin only)

---

## 3. WEBHOOK HANDLER ARCHITECTURE

### 3a. URL Registration

Add to `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/urls.py`:
```python
path("api/webhooks/github/", GithubWebhookEndpoint.as_view()),
```

This lives outside the normal `/api/` namespace to keep it separate from authenticated endpoints.

### 3b. Events to Handle

| GitHub Event | Action | Jet Action |
|---|---|---|
| `issues` | `opened` | Create Jet issue if "Jet" label present, or if bidirectional sync active |
| `issues` | `edited` | Update Jet issue title/description |
| `issues` | `closed` | Update Jet issue state per state_mapping |
| `issues` | `reopened` | Update Jet issue state per state_mapping |
| `issues` | `labeled` | If label is trigger label, create Jet issue; sync labels |
| `issues` | `unlabeled` | Sync label removal |
| `issues` | `assigned` / `unassigned` | Sync assignees via GithubUserMapping |
| `issue_comment` | `created` / `edited` / `deleted` | Sync comments bidirectionally |
| `pull_request` | `opened` | Parse title/body for `[WEB-123]` references, create GithubPullRequest, apply state |
| `pull_request` | `edited` | Re-parse references |
| `pull_request` | `closed` | If merged, apply merged state; otherwise apply closed state |
| `pull_request` | `reopened` | Apply open state |
| `pull_request` | `converted_to_draft` | Apply draft state |
| `pull_request` | `ready_for_review` | Apply open state |
| `pull_request_review` | `submitted` (approved) | Apply approved state |
| `pull_request_review` | `submitted` (request_changes) | Apply review_requested state |
| `label` | `created` / `edited` / `deleted` | Sync label changes |

### 3c. Processing Flow

```
GitHub --> POST /api/webhooks/github/
                |
                v
        [Validate HMAC signature]
                |
                v
        [Look up GithubSyncConfig by installation_id from payload]
                |
                v
        [Return 200 immediately]
                |
                v
        [Enqueue Celery task: process_github_webhook.delay(event, payload, delivery_id)]
                |
                v
        [Celery worker]
            - Create GithubSyncLog (status=processing)
            - Route to specific handler based on event type
            - Acquire advisory lock (per issue/PR to prevent races)
            - Execute sync logic
            - Update GithubSyncLog (status=success/failed)
```

### 3d. HMAC Signature Verification

**File**: `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/utils/integrations/github.py` (extend existing)

```python
def verify_github_webhook_signature(payload_body: bytes, signature_header: str, secret: str) -> bool:
    import hmac
    import hashlib
    expected = "sha256=" + hmac.new(secret.encode(), payload_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature_header)
```

---

## 4. SYNC ENGINE DESIGN

### 4a. Architecture

New directory: `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/bgtasks/github_sync/`

```
github_sync/
    __init__.py
    webhook_handler.py        # Main webhook dispatcher Celery task
    issue_sync.py             # Issue bidirectional sync logic
    comment_sync.py           # Comment sync logic
    pr_handler.py             # PR reference parsing and state automation
    label_sync.py             # Label sync logic  
    state_sync.py             # State mapping logic
    github_api_client.py      # Wrapper around GitHub API calls with token management
    conflict_resolver.py      # Timestamp-based conflict resolution
    reference_parser.py       # [WEB-123] and WEB-123 parsing
```

### 4b. GitHub API Client

Wraps the existing `get_jwt_token()` and `get_github_repos()` patterns from `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/utils/integrations/github.py`, adding:

```python
class GithubAPIClient:
    def __init__(self, workspace_integration: WorkspaceIntegration):
        self.workspace_integration = workspace_integration
        self._token = None
        self._token_expires = None
    
    def _get_installation_token(self) -> str:
        """Get or refresh installation access token."""
        # Uses existing get_jwt_token() + POST to access_tokens_url
    
    def create_issue(self, owner, repo, title, body, labels=None, assignees=None) -> dict
    def update_issue(self, owner, repo, issue_number, **kwargs) -> dict
    def close_issue(self, owner, repo, issue_number) -> dict
    def reopen_issue(self, owner, repo, issue_number) -> dict
    def create_comment(self, owner, repo, issue_number, body) -> dict
    def update_comment(self, owner, repo, comment_id, body) -> dict
    def delete_comment(self, owner, repo, comment_id) -> None
    def get_issue(self, owner, repo, issue_number) -> dict
    def get_pull_request(self, owner, repo, pr_number) -> dict
    def create_label(self, owner, repo, name, color, description="") -> dict
    def list_labels(self, owner, repo) -> list
```

### 4c. Bidirectional Sync Logic

**Jet-to-GitHub** (triggered by Django signals on Issue save or by the issue_activities_task):

The existing `issue_activites_task.py` already posts to PROXY_BASE_URL on every issue activity. Replace the PROXY_BASE_URL call with a native sync call:

In `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/bgtasks/issue_activites_task.py`, at line 1513-1526, replace the PROXY_BASE_URL block:

```python
# Instead of posting to PROXY_BASE_URL, trigger native GitHub sync
if len(issue_activities_created):
    from jet.bgtasks.github_sync.issue_sync import sync_issue_to_github
    for activity in issue_activities_created:
        sync_issue_to_github.delay(
            issue_id=str(activity.issue_id),
            project_id=str(activity.project_id),
            workspace_id=str(activity.workspace_id),
            activity_field=activity.field,
        )
```

**GitHub-to-Jet** (triggered by webhook):

The webhook Celery task dispatches to specific handlers. Each handler:
1. Looks up the GithubIssueSync record
2. Checks `last_synced_at` vs the webhook event timestamp
3. If no existing sync record, creates the Jet entity
4. If existing, updates the Jet entity

### 4d. Conflict Resolution Strategy

**Last-write-wins with source-of-truth preference:**

```python
def should_sync(existing_sync: GithubIssueSync, incoming_timestamp: datetime, direction: str) -> bool:
    """
    Determines if the incoming change should be applied.
    - If last_synced_at is None, always sync
    - If incoming_timestamp > last_synced_at + DEBOUNCE_SECONDS, sync
    - DEBOUNCE_SECONDS = 5 (to prevent echo loops)
    """
    if existing_sync.last_synced_at is None:
        return True
    debounce = timedelta(seconds=5)
    return incoming_timestamp > existing_sync.last_synced_at + debounce
```

**Loop prevention**: Every sync operation updates `last_synced_at`. When the reciprocal webhook/signal fires, the debounce window prevents re-processing. Additionally, changes made by the bot user (the `actor` on GithubRepositorySync) are skipped in the Jet-to-GitHub direction.

### 4e. Label-Based Sync Triggers

**GitHub "Jet" label added**: Webhook `issues.labeled` event. If label name matches `sync_config.github_trigger_label`, create a new Jet issue and GithubIssueSync record.

**Jet "GitHub" label added**: In the `issue_activites_task.py` `track_labels` function (around line ~250 in the file), when a label change is detected and the label matches `sync_config.jet_trigger_label`, enqueue `sync_issue_to_github.delay()` to create the GitHub issue.

---

## 5. PR AUTOMATION DESIGN

### 5a. Reference Parsing

**File**: `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/bgtasks/github_sync/reference_parser.py`

```python
import re

# Matches [WEB-123] - triggers automation
BRACKET_PATTERN = re.compile(r'\[([A-Z]+-\d+)\]')

# Matches bare WEB-123 - link only, no automation
BARE_PATTERN = re.compile(r'(?<!\[)([A-Z]+-\d+)(?!\])')

def parse_issue_references(text: str) -> tuple[list[str], list[str]]:
    """
    Returns (automation_refs, link_refs).
    automation_refs: issue identifiers in brackets [WEB-123]
    link_refs: bare issue identifiers WEB-123
    """
    automation_refs = BRACKET_PATTERN.findall(text)
    # Remove bracket-matched references from bare match
    cleaned_text = BRACKET_PATTERN.sub('', text)
    link_refs = BARE_PATTERN.findall(cleaned_text)
    return automation_refs, link_refs
```

The identifier format uses `Project.identifier` + `-` + `Issue.sequence_id`. To resolve a reference like `WEB-123`:

```python
def resolve_issue_reference(reference: str, workspace_id: uuid) -> Optional[Issue]:
    parts = reference.rsplit('-', 1)
    if len(parts) != 2:
        return None
    identifier, seq = parts[0], int(parts[1])
    return Issue.objects.filter(
        project__identifier=identifier,
        project__workspace_id=workspace_id,
        sequence_id=seq,
    ).first()
```

### 5b. PR State Automation Flow

When a `pull_request` webhook is received:

1. Parse PR title + body for `[WEB-123]` and `WEB-123` references
2. For each bracket reference (`triggers_automation=True`):
   - Create/update GithubPullRequest record
   - Look up `sync_config.pr_state_mapping` for the current PR state
   - If a mapping exists, update the Jet issue's state
   - Create IssueActivity record for the state change (actor = bot user)
3. For each bare reference (`triggers_automation=False`):
   - Create/update GithubPullRequest record
   - Create IssueLink on the Jet issue pointing to the PR URL

### 5c. PR State Mapping Configuration

The `pr_state_mapping` JSON field on GithubSyncConfig stores:

```json
{
    "draft": "uuid-of-jet-state-for-draft",
    "open": "uuid-of-jet-state-for-open",
    "review_requested": "uuid-of-jet-state-for-review",
    "approved": "uuid-of-jet-state-for-approved",
    "merged": "uuid-of-jet-state-for-merged",
    "closed": "uuid-of-jet-state-for-closed"
}
```

The frontend provides a UI that lists the 6 PR lifecycle states and lets the user pick a Jet state from the project's states for each.

---

## 6. FRONTEND COMPONENTS

### 6a. New Service File

**File**: `/Users/sarathfrancis/work/git/innovation_lab/jet/web/services/integrations/github_sync.service.ts`

```typescript
export class GithubSyncService extends APIService {
    // Sync Config CRUD
    async getSyncConfig(workspaceSlug, projectId): Promise<IGithubSyncConfig>
    async createSyncConfig(workspaceSlug, projectId, data): Promise<IGithubSyncConfig>
    async updateSyncConfig(workspaceSlug, projectId, configId, data): Promise<IGithubSyncConfig>
    async activateSync(workspaceSlug, projectId, configId): Promise<void>
    async deactivateSync(workspaceSlug, projectId, configId): Promise<void>
    async triggerManualSync(workspaceSlug, projectId, configId): Promise<void>
    
    // User mappings
    async getUserMappings(workspaceSlug): Promise<IGithubUserMapping[]>
    async createUserMapping(workspaceSlug, data): Promise<IGithubUserMapping>
    async deleteUserMapping(workspaceSlug, mappingId): Promise<void>
    
    // PR list
    async getIssuePullRequests(workspaceSlug, projectId, issueId): Promise<IGithubPullRequest[]>
    
    // Sync logs
    async getSyncLogs(workspaceSlug, projectId): Promise<IGithubSyncLog[]>
}
```

### 6b. New Type Definitions

**File**: `/Users/sarathfrancis/work/git/innovation_lab/jet/web/types/integration.d.ts` (extend existing)

```typescript
export interface IGithubSyncConfig {
    id: string;
    repository_sync: string;
    sync_direction: "bidirectional" | "github_to_jet";
    jet_trigger_label: string | null;
    github_trigger_label: string;
    state_mapping: Record<string, string>;  // github_state -> jet_state_id
    pr_state_mapping: Record<string, string>;  // pr_lifecycle -> jet_state_id
    sync_comments: boolean;
    sync_labels: boolean;
    sync_assignees: boolean;
    is_active: boolean;
}

export interface IGithubPullRequest {
    id: string;
    pr_number: number;
    title: string;
    url: string;
    state: "draft" | "open" | "review_requested" | "approved" | "merged" | "closed";
    issue: string | null;
    triggers_automation: boolean;
    author_login: string;
    author_avatar_url: string | null;
    merged_at: string | null;
    closed_at: string | null;
    created_at: string;
}

export interface IGithubUserMapping { ... }
export interface IGithubSyncLog { ... }
```

### 6c. New Frontend Components

**Directory**: `/Users/sarathfrancis/work/git/innovation_lab/jet/web/components/integration/github/sync/`

| Component | Purpose |
|---|---|
| `sync-config-form.tsx` | Main sync configuration form (direction, triggers, toggles) |
| `state-mapping.tsx` | Map GitHub open/closed to Jet states |
| `pr-state-mapping.tsx` | Map 6 PR lifecycle states to Jet states |
| `sync-status-badge.tsx` | Shows active/inactive sync status |
| `sync-log-list.tsx` | Table of recent sync events with status |
| `user-mapping-form.tsx` | Connect GitHub account / map users |
| `pr-list.tsx` | Shows linked PRs on issue detail sidebar |
| `pr-badge.tsx` | Individual PR status badge with link |

### 6d. Modified Existing Pages

1. **Project Settings Integrations** (`/Users/sarathfrancis/work/git/innovation_lab/jet/web/pages/[workspaceSlug]/projects/[projectId]/settings/integrations.tsx`):
   - Replace current simple `IntegrationCard` with expanded GitHub sync configuration panel
   - Show `sync-config-form`, `state-mapping`, `pr-state-mapping` components
   - Show sync status and recent sync logs

2. **Issue Detail Sidebar** -- add a "GitHub" section showing:
   - Linked PRs (using `pr-list.tsx`)
   - GitHub issue link (if synced)
   - Sync status indicator

3. **Integration Card** (`/Users/sarathfrancis/work/git/innovation_lab/jet/web/components/project/integration-card.tsx`):
   - Add "Configure Sync" button alongside existing "Select Repository"
   - Show sync active/inactive status

4. **Workspace Settings Integrations** (`/Users/sarathfrancis/work/git/innovation_lab/jet/web/pages/[workspaceSlug]/settings/integrations.tsx`):
   - Add user mapping section for GitHub account connection

### 6e. New MobX Store

**File**: `/Users/sarathfrancis/work/git/innovation_lab/jet/web/store/github-sync/github_sync.store.ts`

```typescript
export interface IGithubSyncStore {
    syncConfig: IGithubSyncConfig | null;
    syncLogs: IGithubSyncLog[];
    userMappings: IGithubUserMapping[];
    issuePRs: Record<string, IGithubPullRequest[]>;
    
    fetchSyncConfig(workspaceSlug, projectId): Promise<void>;
    updateSyncConfig(workspaceSlug, projectId, configId, data): Promise<void>;
    fetchSyncLogs(workspaceSlug, projectId): Promise<void>;
    fetchIssuePRs(workspaceSlug, projectId, issueId): Promise<void>;
    fetchUserMappings(workspaceSlug): Promise<void>;
}
```

Register in `RootStore` at `/Users/sarathfrancis/work/git/innovation_lab/jet/web/store/root.ts`.

---

## 7. MIGRATION STRATEGY

### Principle: Additive only, no breaking changes

### Phase 1: Database Migration
- Add new models (GithubSyncConfig, GithubPullRequest, GithubUserMapping, GithubSyncLog)
- Add new fields to GithubIssueSync and GithubCommentSync
- All new fields are nullable or have defaults, so existing data is unaffected
- Existing GithubRepositorySync records continue to work for import-only flow

### Phase 2: Webhook Endpoint
- Add webhook URL outside authenticated routes
- The webhook URL is configured in the GitHub App settings (not per-installation)
- Existing installations get the new endpoint; events are ignored if no GithubSyncConfig exists for the repo

### Phase 3: Backend Sync Engine
- Deploy Celery tasks for sync processing
- The `PROXY_BASE_URL` code path in `issue_activites_task.py` (line 1513) and `importer_task.py` (line 173) remains as-is initially; a new parallel code path is added that runs when a GithubSyncConfig exists
- Gradual deprecation: once native sync is validated, the PROXY_BASE_URL paths can be behind a feature flag

### Phase 4: Frontend
- New sync configuration UI appears only when a GithubRepositorySync exists for the project
- Existing import wizard continues to work unchanged
- New components are additive to the existing project settings integrations page

### Phase 5: Backfill
- Provide a management command `python manage.py github_backfill_sync --project_id=xxx` that:
  - Creates GithubSyncConfig for existing GithubRepositorySync records
  - Fetches current state of all synced issues from GitHub
  - Updates GithubIssueSync records with `github_issue_number` and `last_synced_at`

---

## 8. TESTING APPROACH

### 8a. Unit Tests

**File**: `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/tests/api/test_github_sync.py`

Following the existing `AuthenticatedAPITest` pattern from `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/tests/api/base.py`:

1. **Reference Parser Tests** (pure functions, no DB):
   - `[WEB-123]` extracts automation ref
   - `WEB-123` without brackets extracts link ref
   - Mixed references in PR title + body
   - Edge cases: `[web-123]` (case sensitivity), `[WEB-0]`, overlapping patterns

2. **Webhook Signature Verification Tests**:
   - Valid signature passes
   - Invalid signature rejected
   - Missing header rejected

3. **Conflict Resolution Tests**:
   - `should_sync()` returns True when no prior sync
   - Returns False within debounce window
   - Returns True after debounce window

4. **State Mapping Tests**:
   - GitHub "closed" maps to configured Jet state
   - PR "merged" maps to configured Jet state
   - Missing mapping returns None (no state change)

### 8b. Integration Tests

5. **Webhook Handler Integration**:
   - POST valid webhook with issue.opened event
   - Verify GithubIssueSync record created
   - Verify Jet Issue created with correct fields
   - POST issue.closed event, verify state updated

6. **PR Automation Integration**:
   - POST pull_request.opened with `[WEB-123]` in title
   - Verify GithubPullRequest record created
   - Verify Jet issue state updated
   - POST pull_request.merged, verify final state

7. **Bidirectional Sync Integration**:
   - Create Jet issue with GitHub label
   - Verify GitHub issue creation task enqueued
   - Simulate GitHub webhook for the same issue
   - Verify no loop (debounce prevents re-sync)

### 8c. Mock Strategy

Mock the `GithubAPIClient` HTTP calls using `unittest.mock.patch` on `requests.post` / `requests.get`. The existing codebase uses direct `requests` calls (seen in `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/utils/integrations/github.py`), so patching `requests` is the established pattern.

For Celery tasks, use `CELERY_ALWAYS_EAGER = True` in the test settings (already at `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/settings/test.py`).

---

## IMPLEMENTATION EPICS & STORIES

### Epic 1: Data Layer (Sprint 1, ~3 days)

| Story | Description | Files |
|---|---|---|
| 1.1 | Create new models (GithubSyncConfig, GithubPullRequest, GithubUserMapping, GithubSyncLog) | `apiserver/jet/db/models/integration/github.py` |
| 1.2 | Add new fields to GithubIssueSync, GithubCommentSync | `apiserver/jet/db/models/integration/github.py` |
| 1.3 | Update model __init__ exports | `apiserver/jet/db/models/integration/__init__.py`, `apiserver/jet/db/models/__init__.py` |
| 1.4 | Generate and review migration | `apiserver/jet/db/migrations/0048_github_full_integration.py` |
| 1.5 | Create serializers for new models | `apiserver/jet/api/serializers/integration/github.py`, `apiserver/jet/api/serializers/__init__.py` |

### Epic 2: GitHub API Client (Sprint 1, ~2 days)

| Story | Description | Files |
|---|---|---|
| 2.1 | Build GithubAPIClient class with token management | `apiserver/jet/utils/integrations/github.py` (extend) |
| 2.2 | Add webhook signature verification utility | `apiserver/jet/utils/integrations/github.py` (extend) |
| 2.3 | Add reference parser module | `apiserver/jet/bgtasks/github_sync/reference_parser.py` |
| 2.4 | Unit tests for parser and HMAC verification | `apiserver/jet/tests/api/test_github_sync.py` |

### Epic 3: Webhook Handler (Sprint 2, ~3 days)

| Story | Description | Files |
|---|---|---|
| 3.1 | Create webhook endpoint view with HMAC auth | `apiserver/jet/api/views/integration/github_webhook.py` |
| 3.2 | Register webhook URL in urls.py | `apiserver/jet/urls.py`, `apiserver/jet/api/urls/integration.py` |
| 3.3 | Create webhook dispatcher Celery task | `apiserver/jet/bgtasks/github_sync/webhook_handler.py` |
| 3.4 | Register webhook with GitHub on sync activation | `apiserver/jet/utils/integrations/github.py` |
| 3.5 | Update views __init__ exports | `apiserver/jet/api/views/integration/__init__.py`, `apiserver/jet/api/views/__init__.py` |

### Epic 4: Sync Engine - GitHub to Jet (Sprint 2-3, ~5 days)

| Story | Description | Files |
|---|---|---|
| 4.1 | Issue sync: GitHub issue created/edited -> Jet issue | `apiserver/jet/bgtasks/github_sync/issue_sync.py` |
| 4.2 | Issue sync: GitHub issue closed/reopened -> Jet state change | `apiserver/jet/bgtasks/github_sync/state_sync.py` |
| 4.3 | Label-triggered issue creation (GitHub "Jet" label) | `apiserver/jet/bgtasks/github_sync/issue_sync.py` |
| 4.4 | Comment sync: GitHub comment -> Jet comment | `apiserver/jet/bgtasks/github_sync/comment_sync.py` |
| 4.5 | Label sync: GitHub labels -> Jet labels | `apiserver/jet/bgtasks/github_sync/label_sync.py` |
| 4.6 | Assignee sync via GithubUserMapping | `apiserver/jet/bgtasks/github_sync/issue_sync.py` |
| 4.7 | Conflict resolver module | `apiserver/jet/bgtasks/github_sync/conflict_resolver.py` |
| 4.8 | GithubSyncLog recording for all operations | Across all sync modules |

### Epic 5: Sync Engine - Jet to GitHub (Sprint 3, ~4 days)

| Story | Description | Files |
|---|---|---|
| 5.1 | Replace PROXY_BASE_URL in issue_activities_task with native sync dispatch | `apiserver/jet/bgtasks/issue_activites_task.py` (lines 1512-1526) |
| 5.2 | Jet issue changes -> GitHub issue updates | `apiserver/jet/bgtasks/github_sync/issue_sync.py` |
| 5.3 | Label-triggered GitHub issue creation (Jet "GitHub" label) | `apiserver/jet/bgtasks/github_sync/issue_sync.py` |
| 5.4 | Jet comment changes -> GitHub comment updates | `apiserver/jet/bgtasks/github_sync/comment_sync.py` |
| 5.5 | Loop prevention (bot user detection + debounce) | `apiserver/jet/bgtasks/github_sync/conflict_resolver.py` |

### Epic 6: PR Automation (Sprint 3-4, ~3 days)

| Story | Description | Files |
|---|---|---|
| 6.1 | PR webhook handler (opened, closed, merged, draft, review) | `apiserver/jet/bgtasks/github_sync/pr_handler.py` |
| 6.2 | Reference parsing in PR title/body | `apiserver/jet/bgtasks/github_sync/reference_parser.py` |
| 6.3 | State automation for bracket references | `apiserver/jet/bgtasks/github_sync/pr_handler.py` |
| 6.4 | IssueLink creation for bare references | `apiserver/jet/bgtasks/github_sync/pr_handler.py` |
| 6.5 | PR list API endpoints | `apiserver/jet/api/views/integration/github.py` |

### Epic 7: Backend Configuration APIs (Sprint 4, ~2 days)

| Story | Description | Files |
|---|---|---|
| 7.1 | GithubSyncConfig CRUD endpoints | `apiserver/jet/api/views/integration/github.py` |
| 7.2 | GithubUserMapping CRUD endpoints | `apiserver/jet/api/views/integration/github.py` |
| 7.3 | Sync log list endpoint | `apiserver/jet/api/views/integration/github.py` |
| 7.4 | Manual sync trigger endpoint | `apiserver/jet/api/views/integration/github.py` |
| 7.5 | URL registration for all new endpoints | `apiserver/jet/api/urls/integration.py` |

### Epic 8: Frontend (Sprint 4-5, ~5 days)

| Story | Description | Files |
|---|---|---|
| 8.1 | TypeScript types for new models | `web/types/integration.d.ts` |
| 8.2 | GithubSyncService API service | `web/services/integrations/github_sync.service.ts` |
| 8.3 | GithubSyncStore MobX store + RootStore registration | `web/store/github-sync/github_sync.store.ts`, `web/store/root.ts` |
| 8.4 | Sync configuration form component | `web/components/integration/github/sync/sync-config-form.tsx` |
| 8.5 | State mapping UI component | `web/components/integration/github/sync/state-mapping.tsx` |
| 8.6 | PR state mapping UI component | `web/components/integration/github/sync/pr-state-mapping.tsx` |
| 8.7 | PR list component for issue detail | `web/components/integration/github/sync/pr-list.tsx` |
| 8.8 | Sync log viewer component | `web/components/integration/github/sync/sync-log-list.tsx` |
| 8.9 | User mapping UI component | `web/components/integration/github/sync/user-mapping-form.tsx` |
| 8.10 | Update project settings integrations page | `web/pages/[workspaceSlug]/projects/[projectId]/settings/integrations.tsx` |
| 8.11 | Update integration card component | `web/components/project/integration-card.tsx` |
| 8.12 | Add fetch-keys constants | `web/constants/fetch-keys.ts` |

### Epic 9: Testing & Documentation (Sprint 5, ~3 days)

| Story | Description | Files |
|---|---|---|
| 9.1 | Unit tests for reference parser | `apiserver/jet/tests/api/test_github_sync.py` |
| 9.2 | Unit tests for HMAC verification | `apiserver/jet/tests/api/test_github_sync.py` |
| 9.3 | Unit tests for conflict resolution | `apiserver/jet/tests/api/test_github_sync.py` |
| 9.4 | Integration tests for webhook handler | `apiserver/jet/tests/api/test_github_webhook.py` |
| 9.5 | Integration tests for PR automation | `apiserver/jet/tests/api/test_github_pr.py` |
| 9.6 | Integration tests for bidirectional sync | `apiserver/jet/tests/api/test_github_bidirectional.py` |
| 9.7 | Backfill management command | `apiserver/jet/management/commands/github_backfill_sync.py` |
| 9.8 | Add env vars to .env.example | `.env.example` |

---

## KEY ARCHITECTURAL DECISIONS

1. **Native sync engine replaces PROXY_BASE_URL**: The current architecture delegates sync to an external service that does not exist in self-hosted. The new engine runs entirely within the existing Django + Celery stack.

2. **Advisory locks for concurrency**: Use PostgreSQL advisory locks (via `SELECT pg_advisory_lock()`) per issue/PR to prevent race conditions when multiple webhook events arrive simultaneously.

3. **Bot user pattern preserved**: The existing pattern of creating a bot User + APIToken per workspace integration (seen in `WorkspaceIntegrationViewSet.create()` at line 112) is reused. All sync operations are attributed to the bot user.

4. **Celery for all async processing**: Webhook handler returns 200 immediately and enqueues processing. This matches the existing pattern (e.g., `issue_activites_task`, `importer_task`).

5. **JSON fields for flexible configuration**: State mappings and PR state mappings use JSONField rather than separate models, matching the pattern used in `config` fields on existing models.

6. **Webhook URL at app level, not per-installation**: GitHub Apps have a single webhook URL. The handler determines which workspace/project to route to by looking up the `installation.id` from the webhook payload.

---

### Critical Files for Implementation

- `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/db/models/integration/github.py` - Core models to extend: houses all existing GitHub models (GithubRepository, GithubRepositorySync, GithubIssueSync, GithubCommentSync) and is where all new models (GithubSyncConfig, GithubPullRequest, GithubUserMapping, GithubSyncLog) must be added
- `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/utils/integrations/github.py` - GitHub API utilities to extend: contains JWT token generation, installation metadata fetching, and repo listing that the new GithubAPIClient and webhook verification must build upon
- `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/bgtasks/issue_activites_task.py` - Critical integration point: the PROXY_BASE_URL block (lines 1512-1526) must be augmented with native sync dispatch; also contains the `track_labels` pattern that triggers label-based sync
- `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/api/urls/integration.py` - URL routing: all new endpoints (webhook, sync config, PRs, user mappings, sync logs) must be registered here alongside existing GitHub integration URLs
- `/Users/sarathfrancis/work/git/innovation_lab/jet/web/pages/[workspaceSlug]/projects/[projectId]/settings/integrations.tsx` - Primary frontend entry point: this page currently shows a simple integration card list and must be expanded to host the full sync configuration UI

---

