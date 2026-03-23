# Claude Conversation Log

Session ID: agent-a42b15f2f56f303fd
Date: 2026-03-19 01:58:24

---

## 👤 User

Very thorough exploration of the existing GitHub integration code in /Users/sarathfrancis/work/git/innovation_lab/jet

I need to understand what GitHub integration already exists in this codebase (it was originally Plane, now rebranded to Jet). Search for ALL GitHub-related code:

1. **Backend models**: Read ALL files in `apiserver/jet/db/models/integration/` — especially `github.py` and `base.py`. Document every model, field, and relationship.

2. **Backend views**: Read ALL files in `apiserver/jet/api/views/integration/` — document every endpoint, what it does, HTTP methods, permissions.

3. **Backend URLs**: Read `apiserver/jet/api/urls/integration.py` or similar — document all URL patterns for GitHub integration.

4. **Backend serializers**: Read `apiserver/jet/api/serializers/integration/` — document serializers for GitHub models.

5. **Backend utils**: Read `apiserver/jet/utils/integrations/github.py` — document utility functions for GitHub API calls.

6. **Backend tasks**: Search `apiserver/jet/bgtasks/` for any GitHub-related background tasks (importer, sync, webhooks).

7. **Frontend components**: Search `web/components/integration/` for GitHub-related components. Read them all.

8. **Frontend services**: Search `web/services/integrations/` for GitHub service files. Read them.

9. **Frontend types**: Search for GitHub-related TypeScript types/interfaces.

10. **Importer code**: Read `apiserver/jet/utils/importers/` for any GitHub import functionality.

For each piece of code found, document:
- File path
- What it does
- Key functions/classes/endpoints
- How it connects to other parts
- What's implemented vs. what's missing/stub

Return a comprehensive map of the existing GitHub integration.

---

## 🤖 Claude

I'll conduct a thorough exploration of the GitHub integration code in this codebase. Let me start by searching for all GitHub-related files systematically.

---

## 🤖 Claude

Now let me explore the directory structure to locate all the integration-related files:

---

## 🤖 Claude

Now let me read all the key GitHub integration files. I'll do multiple reads in parallel:

---

## 🤖 Claude

Now let me read the serializers and other integration files:

---

## 🤖 Claude

Now let me read the frontend components and other integration files:

---

## 🤖 Claude

Now let me read the frontend component files to understand the UI flow:

---

## 🤖 Claude

Let me continue reading the remaining GitHub component files:

---

## 🤖 Claude

Let me check the integration service base files and remaining component files:

---

## 🤖 Claude

Now let me search for any importer-related files and check for GitHub webhook or sync functionality:

---

## 🤖 Claude

Let me check for importer views and check for any GitHub-specific sync or webhook code:

---

## 🤖 Claude

Now let me search for any webhook or sync-related code:

---

## 🤖 Claude

Let me check the issue activities task to understand webhook/sync integration:

---

## 🤖 Claude

Let me search for any segway or webhook endpoints:

---

## 🤖 Claude

Let me check what's in the db/models/integration/__init__ to see what's exported:

---

## 🤖 Claude

Perfect! Now let me check what other GitHub component files exist:

---

## 🤖 Claude

Let me also check the frontend types and integration index file:

---

## 🤖 Claude

Perfect! Now let me check the Importer model to understand the data structure:

---

## 🤖 Claude

Excellent! Now let me check the importer serializers:

---

## 🤖 Claude

Perfect! Now let me create a comprehensive report. Let me gather one final piece - check if there are any GitHub-related proxies or external service handlers:

---

## 🤖 Claude

Perfect! I have gathered comprehensive information about the GitHub integration. Let me now provide a thorough analysis.

## GitHub Integration Code Map - Jet (formerly Plane) Codebase

I've completed a thorough exploration of the GitHub integration in the Jet codebase. Here's a comprehensive map of all existing GitHub integration code:

---

### 1. BACKEND MODELS

**Location:** `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/db/models/`

#### Base Integration Models (`base.py`)
- **Integration** (table: `integrations`)
  - Fields: id (UUID), title, provider, network (1=Private, 2=Public), description, author, webhook_url, webhook_secret, redirect_url, metadata, verified, avatar_url
  - Tracks all available integrations (GitHub, Slack, etc.)

- **WorkspaceIntegration** (table: `workspace_integrations`)
  - Fields: workspace, actor (bot user), integration, api_token, metadata, config
  - Unique constraint: [workspace, integration]
  - Represents a workspace's connected instance of an integration

#### GitHub-Specific Models (`github.py`)
- **GithubRepository** (table: `github_repositories`)
  - Fields: name, url, config (JSONField), repository_id (BigInt), owner, project_id, workspace_id, created_at, updated_at
  - Stores metadata about a connected GitHub repository

- **GithubRepositorySync** (table: `github_repository_syncs`)
  - Fields: repository (OneToOne), credentials (JSONField), actor (bot user), workspace_integration (ForeignKey), label (optional)
  - Unique constraint: [project, repository]
  - Manages the sync configuration between a Jet project and GitHub repo

- **GithubIssueSync** (table: `github_issue_syncs`)
  - Fields: repo_issue_id (BigInt), github_issue_id (BigInt), issue_url, issue (ForeignKey), repository_sync (ForeignKey)
  - Unique constraint: [repository_sync, issue]
  - Maps Jet issues to GitHub issues

- **GithubCommentSync** (table: `github_comment_syncs`)
  - Fields: repo_comment_id (BigInt), comment (ForeignKey to IssueComment), issue_sync (ForeignKey)
  - Unique constraint: [issue_sync, comment]
  - Maps Jet comments to GitHub comments

---

### 2. BACKEND VIEWS/ENDPOINTS

**Location:** `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/api/views/`

#### Integration Base Views (`base.py`)
- **IntegrationViewSet**
  - GET /api/integrations/ - List all available integrations
  - POST /api/integrations/ - Create integration
  - GET /api/integrations/<uuid:pk>/ - Retrieve integration
  - PATCH /api/integrations/<uuid:pk>/ - Partial update integration
  - DELETE /api/integrations/<uuid:pk>/ - Delete integration
  - Prevents updates to verified integrations

- **WorkspaceIntegrationViewSet**
  - GET /api/workspaces/<slug>/workspace-integrations/ - List workspace integrations
  - POST /api/workspaces/<slug>/workspace-integrations/<provider>/ - Create workspace integration (creates bot user and API token)
  - GET /api/workspaces/<slug>/workspace-integrations/<uuid:pk>/provider/ - Retrieve
  - DELETE /api/workspaces/<slug>/workspace-integrations/<uuid:pk>/provider/ - Disconnect integration (calls GitHub API to delete installation)

#### GitHub-Specific Views (`github.py`)
- **GithubRepositoriesEndpoint** (GET)
  - Route: /api/workspaces/<slug>/workspace-integrations/<workspace_integration_id>/github-repositories/
  - Returns paginated list of user's GitHub repositories
  - Uses GITHUB_APP credentials to fetch from GitHub API

- **GithubRepositorySyncViewSet**
  - GET /api/workspaces/<slug>/projects/<project_id>/workspace-integrations/<workspace_integration_id>/github-repository-sync/
  - POST: Create repository sync with GitHub repo
    - Input: name, url, config, repository_id, owner, credentials
    - Creates GithubRepository, GithubRepositorySync, "GitHub" label
    - Adds bot user as project member
  - GET/DELETE: Retrieve or delete sync

- **GithubIssueSyncViewSet**
  - GET/POST /api/workspaces/<slug>/projects/<project_id>/github-repository-sync/<repo_sync_id>/github-issue-sync/
  - Creates mappings between Jet issues and GitHub issues

- **BulkCreateGithubIssueSyncEndpoint** (POST)
  - Route: /api/workspaces/<slug>/projects/<project_id>/github-repository-sync/<repo_sync_id>/bulk-create-github-issue-sync/
  - Bulk creates issue sync mappings

- **GithubCommentSyncViewSet**
  - GET/POST /api/workspaces/<slug>/projects/<project_id>/github-repository-sync/<repo_sync_id>/github-issue-sync/<issue_sync_id>/github-comment-sync/
  - Creates mappings between Jet comments and GitHub comments

#### Importer Views (`importer.py`)
- **ServiceIssueImportSummaryEndpoint** (GET)
  - Route: /api/workspaces/<slug>/importers/<service>/
  - For GitHub: Returns issue_count, labels, collaborators from target repo
  - Validates workspace integration exists and has access_tokens_url

- **ImportServiceEndpoint**
  - GET /api/workspaces/<slug>/importers/ - List all imports for workspace
  - POST /api/workspaces/<slug>/projects/importers/<service>/ - Create import job
    - Creates Importer record with status="queued"
    - Triggers async service_importer task
  - DELETE /api/workspaces/<slug>/importers/<service>/<uuid:pk>/ - Delete import and rollback
  - PATCH - Update import status

- **BulkImportIssuesEndpoint** (POST)
  - Route: /api/workspaces/<slug>/projects/<project_id>/importers/<service>/bulk/
  - Bulk creates issues, assignees, labels, comments, links

---

### 3. BACKEND URL ROUTING

**Location:** `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/api/urls/integration.py`

Complete URL patterns defined for:
- Integration CRUD
- WorkspaceIntegration CRUD (with GitHub-specific OAuth flow)
- GitHub repository listing
- GitHub repository sync CRUD
- GitHub issue sync CRUD and bulk create
- GitHub comment sync CRUD
- Slack project sync (separate)

---

### 4. BACKEND SERIALIZERS

**Location:** `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/api/serializers/`

#### Integration Serializers (`base.py`)
- **IntegrationSerializer** - Serializes Integration model (read_only_fields: verified)
- **WorkspaceIntegrationSerializer** - Includes nested integration_detail (IntegrationSerializer)

#### GitHub Serializers (`github.py`)
- **GithubRepositorySerializer** - Serializes GithubRepository model
- **GithubRepositorySyncSerializer** - Includes repo_detail (GithubRepositorySerializer)
- **GithubIssueSyncSerializer** - read_only: project, workspace, repository_sync
- **GithubCommentSyncSerializer** - read_only: project, workspace, repository_sync, issue_sync

#### Importer Serializer (`importer.py`)
- **ImporterSerializer** - Includes nested initiated_by_detail, project_detail, workspace_detail

---

### 5. BACKEND UTILITIES

**Location:** `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/utils/integrations/github.py`

**Key Functions:**
- **get_jwt_token()** - Generates JWT token from GITHUB_APP_ID and GITHUB_APP_PRIVATE_KEY env vars
- **get_github_metadata(installation_id)** - Fetches installation metadata
- **get_github_repos(access_tokens_url, repositories_url)** - Lists user's repositories
- **delete_github_installation(installation_id)** - Uninstalls GitHub app
- **get_github_repo_details(access_tokens_url, owner, repo)** - Returns open_issues_count, total_labels, collaborators
- **get_release_notes()** - Fetches Jet release notes from GitHub API (only 100 collaborators supported, TODO comment)

---

### 6. BACKGROUND TASKS

**Location:** `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/bgtasks/`

#### Importer Task (`importer_task.py`)
- **service_importer(service, importer_id)** - Celery shared_task
  - Handles both GitHub and Jira imports
  - For GitHub with sync=True:
    - Creates GithubRepository and GithubRepositorySync records
    - Adds bot user to project
    - Creates/reuses "GitHub" label
  - User handling: Bulk creates workspace/project members for invited users
  - Calls PROXY_BASE_URL webhook: `/hooks/workspaces/{workspace_id}/projects/{project_id}/importers/{service}/`

#### Issue Activities Task (`issue_activites_task.py`)
- Tracks issue changes and calls PROXY_BASE_URL webhook for integrations: `/hooks/workspaces/{workspace_id}/projects/{project_id}/issues/{issue_id}/issue-activity-hooks/`
- Comment: "Post the updates to segway for integrations and webhooks"

---

### 7. FRONTEND COMPONENTS

**Location:** `/Users/sarathfrancis/work/git/innovation_lab/jet/web/components/integration/github/`

#### Main Orchestrator (`root.tsx` - GithubImporterRoot)
- Manages 5-step import workflow
- Form state management with react-hook-form
- Steps: Configure -> Import Data -> Repo Details -> Import Users -> Confirm
- Calls GithubIntegrationService.createGithubServiceImport() on submit

#### Step Components:
1. **import-configure.tsx** (GithubImportConfigure)
   - Shows GitHub auth status
   - Validates workspace integration exists

2. **import-data.tsx** (GithubImportData)
   - SelectRepository component (paginated, infinite scroll)
   - Project selection
   - Sync toggle

3. **repo-details.tsx** (GithubRepoDetails)
   - Fetches and displays: issue count, labels, collaborators
   - Initializes user list from collaborators

4. **import-users.tsx** (GithubImportUsers)
   - Maps collaborators to Jet users
   - Options: "Map to existing", "Invite by email", "Do not import"

5. **import-confirm.tsx** (GithubImportConfirm)
   - Final confirmation before import

#### Supporting Components:
- **auth.tsx** (GithubAuth) - OAuth integration button (uses useIntegrationPopup hook)
- **select-repository.tsx** (SelectRepository) - Paginated repository picker with infinite scroll
- **single-user-select.tsx** (SingleUserSelect) - User mapping/invitation UI

---

### 8. FRONTEND SERVICES

**Location:** `/Users/sarathfrancis/work/git/innovation_lab/jet/web/services/integrations/`

#### GitHub Service (`github.service.ts` - GithubIntegrationService)
- **listAllRepositories(workspaceSlug, integrationSlug)** - GET /api/workspaces/{slug}/workspace-integrations/{id}/github-repositories
- **getGithubRepoInfo(workspaceSlug, {owner, repo})** - GET /api/workspaces/{slug}/importers/github/
- **createGithubServiceImport(workspaceSlug, data, user)** - POST /api/workspaces/{slug}/projects/importers/github/

#### Integration Service (`integration.service.ts` - IntegrationService)
- **getAppIntegrationsList()** - GET /api/integrations/
- **getWorkspaceIntegrationsList(workspaceSlug)** - GET /api/workspaces/{slug}/workspace-integrations/
- **deleteWorkspaceIntegration(workspaceSlug, integrationId)** - DELETE
- **getImporterServicesList(workspaceSlug)** - GET /api/workspaces/{slug}/importers/
- **deleteImporterService(workspaceSlug, service, importerId, user)** - DELETE (tracks event)

---

### 9. FRONTEND TYPES/INTERFACES

**Location:** `/Users/sarathfrancis/work/git/innovation_lab/jet/web/types/`

#### GitHub Importer Types (`importer/github-importer.d.ts`)
- **IGithubServiceImportFormData** - Form submission payload
  - metadata: {owner, name, repository_id, url}
  - data: {users: [{username, import, email}]}
  - config: {sync: boolean}
  - project_id: string

- **IGithubRepoCollaborator** - {avatar_url, html_url, id, login, url}

- **IGithubRepoInfo** - {issue_count, labels, collaborators[]}

#### Integration Types (`integration.d.ts`)
- **IAppIntegration** - All integration metadata fields
- **IWorkspaceIntegration** - Workspace-specific integration instance

#### Importer Types (`importer/index.ts`)
- **IImporterService** - Import job record with metadata, status, config

---

### 10. ARCHITECTURE OVERVIEW

#### Authentication Flow
1. User initiates GitHub integration on workspace
2. Frontend calls `useIntegrationPopup(provider)` hook
3. OAuth popup creates WorkspaceIntegration with bot user
4. Bot user gets APIToken for API calls
5. Stores installation_id and metadata (access_tokens_url, etc.)

#### Import Flow
1. User selects repository and project
2. Frontend fetches repo metadata (issues, labels, collaborators)
3. User maps collaborators to Jet users
4. On submit: Creates Importer record with status="queued"
5. service_importer task processes asynchronously
6. Creates issues via proxy service at PROXY_BASE_URL
7. If sync=True, creates GithubRepositorySync for bidirectional sync

#### Sync Architecture
- **One-way import**: Issues imported from GitHub to Jet
- **Optional two-way**: GithubRepositorySync, GithubIssueSync, GithubCommentSync models exist but appear to be primarily for tracking which issues are synced
- **External proxy service**: PROXY_BASE_URL handles actual GitHub API interactions and issue creation
- **Webhook integration**: Issue changes trigger webhooks to proxy service for integration syncing

---

### 11. WHAT'S IMPLEMENTED

- OAuth GitHub app authentication
- Repository selection and browsing (with pagination)
- Repository metadata inspection (issues, labels, collaborators)
- User mapping/invitation workflow
- Bulk import of issues, labels, comments, assignees
- Import status tracking
- Bot user creation and project member assignment
- GitHub label synchronization
- Bidirectional sync model structure (but actual sync logic in proxy service)

### 12. WHAT'S MISSING/STUBBED

- **No direct webhook handling** - All webhook logic delegated to external PROXY_BASE_URL service
- **No GitHub comment sync implementation** - Model exists but no endpoints for syncing comment changes
- **Limited to 100 collaborators** - TODO comment in get_github_repo_details
- **No Jira importer** - Only stub references (jira_project_issue_summary function exists)
- **No export/push-to-GitHub** - Only one-way imports supported
- **No real-time sync** - Requires manual trigger via import flow

---

### 13. KEY FILES SUMMARY

**Backend Files:**
- `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/db/models/integration/github.py` (99 lines)
- `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/api/views/integration/github.py` (201 lines)
- `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/api/views/integration/base.py` (165 lines)
- `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/utils/integrations/github.py` (153 lines)
- `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/bgtasks/importer_task.py` (195 lines)
- `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/api/urls/integration.py` (151 lines)

**Frontend Files:**
- `/Users/sarathfrancis/work/git/innovation_lab/jet/web/components/integration/github/root.tsx` (258 lines)
- `/Users/sarathfrancis/work/git/innovation_lab/jet/web/services/integrations/github.service.ts` (50 lines)
- 8 additional component files (auth, import-configure, import-data, repo-details, import-users, import-confirm, select-repository, single-user-select)

**Type Definitions:**
- `/Users/sarathfrancis/work/git/innovation_lab/jet/web/types/importer/github-importer.d.ts` (34 lines)
- `/Users/sarathfrancis/work/git/innovation_lab/jet/web/types/integration.d.ts` (77 lines)

This comprehensive integration provides a solid foundation for GitHub repository importing with a clean separation between the Jet backend, frontend UI, and an external proxy service that handles the actual GitHub API interactions.

---

