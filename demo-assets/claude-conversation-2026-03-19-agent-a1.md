# Claude Conversation Log

Session ID: agent-a18fd0cc131c305a1
Date: 2026-03-19 03:02:27

---

## 👤 User

I need to understand the codebase structure for the Jet project. Please explore:

1. List all files in `apiserver/jet/bgtasks/` directory
2. Read `apiserver/jet/bgtasks/issue_activites_task.py` around line 1500-1530 to find the PROXY_BASE_URL block
3. List all files in `web/services/integrations/` directory
4. Read `web/services/integrations/github.service.ts`
5. Read `web/types/integration.d.ts` or similar type files for integrations
6. List files in `web/components/integration/github/` directory
7. Check the latest migration number in `apiserver/jet/db/migrations/` to determine the next migration number
8. Read `apiserver/jet/api/views/integration/base.py` around line 100-120 to understand bot user pattern
9. Read `apiserver/jet/api/views/base.py` to understand BaseViewSet and BaseAPIView

Be thorough in exploring all these areas.

---

## 🤖 Claude

I'll explore the Jet project codebase systematically. Let me start with these searches in parallel.

---

## 🤖 Claude

Now let me read the issue_activites_task.py file around lines 1500-1530 and also check the file structure for other directories:

---

## 🤖 Claude

Good! Now let me read the service files and type definitions:

---

## 🤖 Claude

Now let me read the base.py file and check the integration views directory:

---

## 🤖 Claude

Now let me read the integration base.py and github.py files:

---

## 🤖 Claude

Let me check the db models directory:

---

## 🤖 Claude

Now let me read the integration models and check more details:

---

## 🤖 Claude

Perfect! Let me now get more context about the integration utils and check web components:

---

## 🤖 Claude

Let me read the github utils file and check the web component structure more thoroughly:

---

## 🤖 Claude

Let me read one more web component example and check the serializers:

---

## 🤖 Claude

Perfect! Now let me create a comprehensive summary. Let me check a couple more things to be thorough:

---

## 🤖 Claude

Now let me generate a comprehensive report with all the findings:

## Jet Project Codebase Structure - Comprehensive Exploration Report

I've thoroughly explored the Jet project codebase. Here's the complete structural breakdown:

### 1. Background Tasks Directory
**Location:** `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/bgtasks/`

**Files:**
- `issue_activites_task.py` (47,307 bytes) - Primary file with PROXY_BASE_URL integration
- `export_task.py` - Data export functionality
- `importer_task.py` - Import task handling
- `analytic_plot_export.py` - Analytics exports
- `notification_task.py` - Notification processing
- `email_verification_task.py`
- `forgot_password_task.py`
- `magic_link_code_task.py`
- `project_invitation_task.py`
- `user_welcome_task.py`
- `workspace_invitation_task.py`
- `issue_automation_task.py`
- `exporter_expired_task.py`

**PROXY_BASE_URL Usage in issue_activites_task.py:**
- Located at line 1513: `if settings.PROXY_BASE_URL:`
- Lines 1514-1524: Posts issue activity updates to webhook endpoint
- Format: `f"{settings.PROXY_BASE_URL}/hooks/workspaces/{workspace_id}/projects/{project_id}/issues/{issue_id}/issue-activity-hooks/"`

### 2. Web Services/Integrations Directory
**Location:** `/Users/sarathfrancis/work/git/innovation_lab/jet/web/services/integrations/`

**Files:**
- `github.service.ts` - GithubIntegrationService class (50 lines)
  - Methods: `listAllRepositories()`, `getGithubRepoInfo()`, `createGithubServiceImport()`
- `integration.service.ts` - Main IntegrationService class (80 lines)
  - Methods: `getAppIntegrationsList()`, `getWorkspaceIntegrationsList()`, `deleteWorkspaceIntegration()`, `getImporterServicesList()`, `getExportsServicesList()`, `deleteImporterService()`
- `jira.service.ts` - Jira integration
- `index.ts` - Exports all services

### 3. Web Type Definitions
**Location:** `/Users/sarathfrancis/work/git/innovation_lab/jet/web/types/integration.d.ts`

**Interfaces:**
- `IAppIntegration` - App integration metadata (author, avatar_url, provider, webhook_secret, webhook_url, verified, etc.)
- `IWorkspaceIntegration` - Workspace-level integration (workspace, actor, integration, api_token, metadata, config)
- `ISlackIntegration` - Slack-specific integration with bot_user_id, access_token, team_id
- `ISlackIntegrationData` - Slack OAuth response structure

### 4. Web Components - GitHub Integration
**Location:** `/Users/sarathfrancis/work/git/innovation_lab/jet/web/components/integration/github/`

**Components:**
- `root.tsx` - Main orchestrator (GithubImporterRoot) - 258 lines
  - Manages 5-step workflow: Configure → Import Data → Issues → Users → Confirm
  - Uses react-hook-form with TFormValues type
  - Integrates with IntegrationService and GithubIntegrationService
- `import-configure.tsx` - Configuration step
- `import-data.tsx` - Data import configuration
- `import-confirm.tsx` - Confirmation dialog
- `import-users.tsx` - User mapping interface
- `repo-details.tsx` - Repository information display
- `select-repository.tsx` - Repository selection
- `single-user-select.tsx` - Individual user selection
- `auth.tsx` - OAuth authentication
- `index.ts` - Exports

**Other Integration Components:**
- `delete-import-modal.tsx` - Delete confirmation
- `guide.tsx` - Import guide
- `single-integration-card.tsx` - Card display
- `single-import.tsx` - Single import form
- Jira components in `jira/` directory
- Slack component in `slack/select-channel.tsx`

### 5. API Migrations
**Location:** `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/db/migrations/`

**Latest Migration:** `0047_update_content_types.py` (March 18, 2024, 17:39)

**Recent Migrations:**
- 0046 - analyticview updates
- 0045 - issueactivity_epoch, workspacemember_issue_props
- 0044 - auto_20230913_0709
- 0043/0042 - analyticview_created_by modifications
- 0041 - cycle_sort_order, issuecomment_access

**Next Migration Number:** 0048

### 6. API Views - Integration Base
**Location:** `/Users/sarathfrancis/work/git/innovation_lab/jet/api/views/integration/base.py`

**ViewSets:**
- `IntegrationViewSet(BaseViewSet)` - Lines 30-67
  - Methods: create, partial_update, destroy
  - Prevents updates to verified integrations
- `WorkspaceIntegrationViewSet(BaseViewSet)` - Lines 70-164
  - Permission: WorkSpaceAdminPermission
  - Method: create (lines 86-149) - Creates bot user with UUID email, APIToken, WorkspaceMember
  - Method: destroy (lines 151-164) - Handles GitHub uninstallation

**Bot User Creation Pattern (lines 111-145):**
- Email: `{uuid.uuid4().hex}@jetpm.app`
- Username: Random UUID
- Password: Random UUID
- is_bot: True
- Role: 20 (highest privilege)
- Creates separate APIToken with user_type=1

### 7. API Views - Base Classes
**Location:** `/Users/sarathfrancis/work/git/innovation_lab/jet/api/views/base.py` (193 lines)

**BaseViewSet:**
- Inherits: TimezoneMixin, ModelViewSet, BasePaginator
- Properties: `workspace_slug`, `project_id`
- Includes: exception handling, query logging (DEBUG mode)
- Filter backends: DjangoFilterBackend, SearchFilter

**BaseAPIView:**
- Similar structure to BaseViewSet but extends APIView
- Has filter_queryset method

**TimezoneMixin:**
- Activates user's timezone in initial() method

### 8. API Views - GitHub Integration
**Location:** `/Users/sarathfrancis/work/git/innovation_lab/jet/api/views/integration/github.py` (201 lines)

**Endpoints:**
- `GithubRepositoriesEndpoint(BaseAPIView)` - GET repositories (lines 27-50)
- `GithubRepositorySyncViewSet(BaseViewSet)` - CRUD for repository syncs (lines 53-141)
  - Creates Label "GitHub" with color "#003773"
  - Adds bot as ProjectMember with role=20
- `GithubIssueSyncViewSet(BaseViewSet)` - Issue synchronization (lines 144-156)
- `BulkCreateGithubIssueSyncEndpoint(BaseAPIView)` - Bulk create syncs (lines 159-184)
- `GithubCommentSyncViewSet(BaseViewSet)` - Comment synchronization (lines 187-200)

### 9. Database Models - Integration
**Location:** `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/db/models/integration/`

**Base Models (base.py):**
- `Integration` - UUID primary key, provider (unique), title, network (1=Private, 2=Public), metadata, verified, webhook_secret, redirect_url, avatar_url
- `WorkspaceIntegration` - Workspace FK, actor (bot user) FK, integration FK, api_token FK, metadata, config

**GitHub Models (github.py):**
- `GithubRepository` - name, url, config, repository_id, owner
- `GithubRepositorySync` - repository (OneToOne), credentials, actor FK, workspace_integration FK, label FK
- `GithubIssueSync` - repo_issue_id, github_issue_id, issue_url, issue FK, repository_sync FK
- `GithubCommentSync` - repo_comment_id, comment FK, issue_sync FK

**Slack Models (slack.py):**
- Basic slack integration structure

### 10. Serializers
**Location:** `/Users/sarathfrancis/work/git/innovation_lab/jet/api/serializers/integration/`

**Base Serializers:**
- `IntegrationSerializer(BaseSerializer)` - All fields, verified is read_only
- `WorkspaceIntegrationSerializer(BaseSerializer)` - All fields, includes nested `integration_detail`

**GitHub Serializers:**
- `GithubRepositorySerializer` - All fields
- `GithubRepositorySyncSerializer` - All fields with nested `repo_detail`
- `GithubIssueSyncSerializer` - project, workspace, repository_sync are read_only
- `GithubCommentSyncSerializer` - project, workspace, repository_sync, issue_sync are read_only

### 11. Utilities
**Location:** `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/utils/integrations/`

**GitHub Utilities (github.py - 153 lines):**
- `get_jwt_token()` - Generates JWT using GITHUB_APP_ID and GITHUB_APP_PRIVATE_KEY
- `get_github_metadata(installation_id)` - Fetches installation metadata from GitHub API
- `get_github_repos(access_tokens_url, repositories_url)` - Lists repositories
- `delete_github_installation(installation_id)` - Uninstalls GitHub app
- `get_github_repo_details(owner, repo)` - Fetches open_issues, total_labels, collaborators
- `get_release_notes()` - Fetches latest 5 releases from makeplane/jet repo

**Key Environment Variables:**
- GITHUB_APP_ID
- GITHUB_APP_PRIVATE_KEY
- GITHUB_ACCESS_TOKEN (optional, for unauthenticated requests fallback)

### 12. Integration API URLs
**Location:** `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/api/urls/integration.py` (4,549 bytes)

### 13. Web Constants
**Location:** `/Users/sarathfrancis/work/git/innovation_lab/jet/web/constants/fetch-keys.ts`

References used: `APP_INTEGRATIONS`, `WORKSPACE_INTEGRATIONS()`, `IMPORTER_SERVICES_LIST()`, `WORKSPACE_INTEGRATIONS()`

---

## Key Architectural Patterns

1. **Bot User Pattern:** Each workspace integration creates a dedicated bot user with UUID email (@jetpm.app domain) and APIToken for service-to-service communication

2. **Webhook Integration:** PROXY_BASE_URL environment variable routes issue activity updates to external webhook handlers

3. **Multi-Step Integration Workflow:** Frontend implements 5-step configuration process for GitHub imports

4. **Sync Models:** Separate sync models (GithubRepositorySync, GithubIssueSync, GithubCommentSync) maintain bidirectional data mapping

5. **Service Layer:** Separate service classes in TypeScript encapsulate API communication logic

6. **Permission Hierarchy:** WorkSpaceAdminPermission controls integration management; Bot users get role=20

---

