# Claude Conversation Log

Session ID: agent-ac4cef84139b13030
Date: 2026-03-19 03:11:28

---

## 👤 User

Explore the Jet frontend to understand patterns for building new integration features. Be thorough:

1. Read `web/services/integrations/github.service.ts` completely
2. Read `web/services/integrations/integration.service.ts` completely
3. Read `web/services/integrations/index.ts`
4. Read `web/types/integration.d.ts` completely
5. Read `web/store/root.ts` to understand store registration
6. Find any existing MobX stores for integrations (glob for `*integration*store*` or `*github*store*`)
7. Read `web/helpers/fetch-wrapper.ts` or `web/helpers/api.helper.ts` or similar API helper to understand HTTP client patterns
8. Read `web/services/api.service.ts` or the base service class to understand how services make API calls
9. Check `web/components/integration/github/root.tsx` to see existing component patterns
10. List all files in `web/store/` to understand store naming patterns

Return all file contents and patterns found.

---

## 🤖 Claude

I'll explore the Jet frontend to understand integration patterns. Let me start by reading the files you specified and finding related files.

---

## 🤖 Claude

Now let me read the GitHub integration component and look for more integration-related files:

---

## 🤖 Claude

Now let me read the Jira service to understand patterns and check for more component examples:

---

## 🤖 Claude

Let me check for more integration patterns and look at the type definitions more completely:

---

## 🤖 Claude

Let me read the importer types file:

---

## 🤖 Claude

Let me look for more type definitions and check the GitHub integration component files:

---

## 🤖 Claude

Now let me check the importer type definitions:

---

## 🤖 Claude

Let me check more integration components and the hooks:

---

## 🤖 Claude

Let me read the hook and check for more patterns:

---

## 🤖 Claude

Now let me check for additional helper patterns and structure:

---

## 🤖 Claude

Let me check for more Jira components and the structure:

---

## 🤖 Claude

Let me check the Slack component and look for any additional patterns:

---

## 🤖 Claude

Let me check the importer types:

---

## 🤖 Claude

Perfect! Now let me check for any other important helper patterns and summary information:

---

## 🤖 Claude

Perfect! Now let me compile a comprehensive summary of all the patterns found. Let me create one final comprehensive report:

## Comprehensive Jet Frontend Integration Feature Patterns

Based on my thorough exploration of the Jet frontend codebase, here are the complete patterns for building new integration features:

### Core Architecture Overview

**File Structure:**
- Services: `/web/services/integrations/` (base service class extends APIService)
- Components: `/web/components/integration/{github,jira,slack}/` (feature-specific sub-folders)
- Types: `/web/types/integration.d.ts` and `/web/types/importer/`
- Store: `/web/store/root.ts` (MobX store registry)
- Hooks: `/web/hooks/use-integration-popup.tsx`

### 1. Integration Service Pattern

**Base Service Class** (`/web/services/api.service.ts`):
- Abstract class using axios
- Manages access tokens via cookies
- Methods: `get()`, `post()`, `put()`, `patch()`, `delete()`, `request()`
- Header construction with Bearer token auth

**Integration Service** (`/web/services/integrations/integration.service.ts`):
- Extends APIService
- Methods for managing workspace and app integrations:
  - `getAppIntegrationsList()` → List all available integrations
  - `getWorkspaceIntegrationsList(workspaceSlug)` → Workspace-specific integrations
  - `deleteWorkspaceIntegration(workspaceSlug, integrationId)` → Disconnect integration
  - `getImporterServicesList(workspaceSlug)` → List import jobs
  - `getExportsServicesList(workspaceSlug, cursor, per_page)` → Paginated exports
  - `deleteImporterService(workspaceSlug, service, importerId, user)` → Remove import

**Provider-Specific Services** (GitHub & Jira examples):
- `GithubIntegrationService` extends APIService
- `JiraImporterService` extends APIService
- Pattern: Service for each external provider with provider-specific methods
- Methods call provider-specific API endpoints
- Track events on completion via `TrackEventService`

**Key Paths:**
- `/api/integrations/` (list all)
- `/api/workspaces/{slug}/workspace-integrations/` (workspace integrations)
- `/api/workspaces/{slug}/workspace-integrations/{id}/github-repositories` (GitHub repos)
- `/api/workspaces/{slug}/importers/{service}/` (import details)
- `/api/workspaces/{slug}/projects/importers/{service}/` (create import)

### 2. Type Definitions Pattern

**Core Integration Types** (`/web/types/integration.d.ts`):
```
IAppIntegration: {
  provider, title, webhook_url, verified, avatar_url, metadata, etc.
}

IWorkspaceIntegration: {
  id, workspace, integration, integration_detail, api_token, config, metadata
}

ISlackIntegration: {
  access_token, bot_user_id, webhook_url, team_id, etc.
}
```

**Importer Types** (`/web/types/importer/`):
```
IImporterService: {
  id, service (github/jira), status (processing/completed/failed),
  metadata, config, data, created_at, initiated_by_detail, project_detail
}

IGithubServiceImportFormData: {
  metadata: { owner, name, repository_id, url },
  data: { users[] },
  config: { sync: boolean },
  project_id
}

IJiraImporterForm: {
  metadata: IJiraMetadata,
  config: IJiraConfig (epics_to_modules),
  data: IJiraData,
  project_id
}

IGithubRepoInfo: {
  issue_count, labels, collaborators[]
}

IGithubRepoCollaborator: {
  login, avatar_url, id, html_url
}
```

### 3. Component Architecture Pattern

**Multi-Step Workflow Pattern** (used in GitHub & Jira):
```
TIntegrationSteps type union:
  - "import-configure"
  - "import-data"
  - "repo-details" / "display-import-data"
  - "import-users"
  - "import-confirm"

IIntegrationData:
  state: TIntegrationSteps
```

**Root Component Structure** (e.g., `GithubImporterRoot`):
- useState for current step tracking
- useForm from react-hook-form with controller
- useSWR for data fetching (integration list, workspace integrations)
- Workflow visualization showing progress steps
- Conditional rendering of sub-components per step
- Form submission creates import via service

**Typical Sub-Component Props Pattern:**
```typescript
type Props = {
  handleStepChange: (value: TIntegrationSteps) => void;
  [other integration-specific props]
}
```

**Component Export Pattern** (`/web/components/integration/github/index.ts`):
```
export * from "./auth";
export * from "./import-configure";
export * from "./import-confirm";
export * from "./import-data";
export * from "./import-users";
export * from "./repo-details";
export * from "./root";
export * from "./select-repository";
export * from "./single-user-select";
```

### 4. Key Components Breakdown

**Authentication Component** (`auth.tsx`):
- Uses `useIntegrationPopup` hook
- Button showing connection status
- Disabled after successful connection

**Configure Component** (`import-configure.tsx`):
- Shows authentication button
- Validates workspace integration is connected
- Progresses to next step

**Data Selection Component** (`import-data.tsx`):
- uses MobX store observer pattern
- `useMobxStore()` to access project store
- Controller with CustomSearchSelect for repository selection
- Controller with ToggleSwitch for sync option
- Validates repo and project before progression

**Repository Selection Component** (`select-repository.tsx`):
- useSWRInfinite for paginated data fetching
- Pagination URL pattern: `/api/workspaces/{slug}/workspace-integrations/{id}/github-repositories/?page={pageIndex}`
- CustomSearchSelect with footer option for "load more"
- Maps data to select options

**Repo Details Component** (`repo-details.tsx`):
- useSWR to fetch repo info via `githubIntegrationService.getGithubRepoInfo()`
- Displays issue count, labels, collaborators
- Uses setValue from form to populate collaborators

**Import Users Component** (`import-users.tsx`):
- Manages user mapping (map, invite, skip)
- SingleUserSelect sub-component for individual user mapping
- Maps GitHub collaborators to workspace users

**Confirm Component** (`import-confirm.tsx`):
- Summary of selected options
- Final confirmation before submission

### 5. Hook Pattern

**useIntegrationPopup** (`/web/hooks/use-integration-popup.tsx`):
```typescript
const useIntegrationPopup = (provider: string | undefined, stateParams?: string) => {
  // Returns: { startAuth, isConnecting }
  // Opens OAuth popup for provider (github, slack, slackChannel)
  // providerUrls object maps provider to OAuth URL
  // Checks popup status with polling interval
}
```

**Provider URLs pattern:**
```
github: GitHub Apps installation URL with workspace state
slack: Slack OAuth with scopes
slackChannel: Slack incoming webhook scope
```

### 6. Store Integration Pattern

**MobX Store Provider** (`/web/lib/mobx/store-provider.tsx`):
```typescript
export const useMobxStore = () => useContext(MobxStoreContext);
// Returns RootStore instance with all registered stores
```

**Store Registration** (`/web/store/root.ts`):
- Constructor instantiates all domain stores
- No separate integration store currently
- Components access `projectStore.projects[workspaceSlug]` for project list

### 7. Data Fetching Pattern

**SWR Fetch Keys** (`/web/constants/fetch-keys.ts`):
```
APP_INTEGRATIONS: "APP_INTEGRATIONS"
WORKSPACE_INTEGRATIONS(slug): "WORKSPACE_INTEGRATIONS_{SLUG}"
IMPORTER_SERVICES_LIST(slug): "IMPORTER_SERVICES_LIST_{SLUG}"
GITHUB_REPOSITORY_INFO(slug, repoName): "GITHUB_REPOSITORY_INFO_{SLUG}_{REPONAME}"
SLACK_CHANNEL_INFO(slug, projectId): "SLACK_CHANNEL_INFO_{SLUG}_{PROJECT_ID}"
```

**Mutation Pattern:**
```typescript
import useSWR, { mutate } from "swr";

// Optimistic update:
mutate<T[]>(
  FETCH_KEY,
  (prevData) => prevData?.filter(item => item.id !== itemToDelete.id),
  false // revalidate: false
);

// Then call API
service.delete()
  .then(() => mutate(FETCH_KEY))
  .catch(() => mutate(FETCH_KEY)); // Revert on error
```

### 8. Form Pattern (React Hook Form)

**Basic Setup:**
```typescript
const { handleSubmit, control, setValue, watch } = useForm<TFormValues>({
  defaultValues: defaultFormValues,
});
```

**Controller Usage:**
```typescript
<Controller
  control={control}
  name="field_name"
  rules={{ required: "validation message" }}
  render={({ field: { value, onChange, ref } }) => (
    <CustomComponent value={value} onChange={onChange} />
  )}
/>
```

**Jira-Specific:** Uses `FormProvider` + `useFormContext` pattern for complex nested forms

### 9. Integration Card Component Pattern

**SingleIntegrationCard** (`/web/components/integration/single-integration-card.tsx`):
- Displays integration with logo and description
- Shows install/uninstall buttons
- Tracks installed status via workspace integrations list
- Uses `useIntegrationPopup` for OAuth
- Handles deletion with mutation

### 10. Import Management Pattern

**Guide Component** (`/web/components/integration/guide.tsx`):
- Lists available importers from `IMPORTERS_EXPORTERS_LIST` constant
- Shows previous imports from `getImporterServicesList()`
- Routes to provider-specific importer root on selection
- Renders SingleImport components for past jobs

**SingleImport Component** (`/web/components/integration/single-import.tsx`):
- Shows status badge (processing/completed/failed)
- Displays metadata (date, initiated by)
- Delete button with modal confirmation

**DeleteImportModal** (`/web/components/integration/delete-import-modal.tsx`):
- Confirmation flow with type-to-confirm pattern
- Calls `integrationService.deleteImporterService()`
- Tracks deletion event
- Optimistic update before API call

### 11. UI Library Pattern

Uses Jet UI components (`@jet/ui`):
- Button, CustomSearchSelect, CustomSelect, ToggleSwitch, Input, Loader
- Dialog (from @headlessui/react) for modals
- Icons from lucide-react

### 12. Workspace/Provider Config Constants

**Importers List** (`/web/constants/workspace.ts`):
```typescript
IMPORTERS_EXPORTERS_LIST = [
  { provider: "github", type: "import", title, description, logo },
  { provider: "jira", type: "import", title, description, logo }
]
```

### 13. Event Tracking Pattern

**TrackEventService Integration:**
- Called on successful import creation
- Event names: "GITHUB_IMPORTER_CREATE", "JIRA_IMPORTER_CREATE"
- Passes user object for attribution

### 14. API Response Error Handling Pattern

Standard pattern across services:
```typescript
async method(params) {
  return this.get(url, config)
    .then((response) => response?.data)
    .catch((error) => {
      throw error?.response?.data;
    });
}
```

---

## Summary Statistics

**Integration Services:** 3 (Integration base, GitHub, Jira)
**Integration Components:** 23+ files across github/jira/slack/general integration folders
**Store Patterns:** MobX with context provider
**Data Fetching:** SWR with fetch keys constants
**Forms:** React Hook Form with controlled components
**Type Safety:** Comprehensive TypeScript interfaces for all data structures

All absolute file paths for reference:
- `/Users/sarathfrancis/work/git/innovation_lab/jet/web/services/integrations/github.service.ts`
- `/Users/sarathfrancis/work/git/innovation_lab/jet/web/services/integrations/integration.service.ts`
- `/Users/sarathfrancis/work/git/innovation_lab/jet/web/services/integrations/jira.service.ts`
- `/Users/sarathfrancis/work/git/innovation_lab/jet/web/services/api.service.ts`
- `/Users/sarathfrancis/work/git/innovation_lab/jet/web/types/integration.d.ts`
- `/Users/sarathfrancis/work/git/innovation_lab/jet/web/types/importer/index.ts`
- `/Users/sarathfrancis/work/git/innovation_lab/jet/web/types/importer/github-importer.d.ts`
- `/Users/sarathfrancis/work/git/innovation_lab/jet/web/types/importer/jira-importer.d.ts`
- `/Users/sarathfrancis/work/git/innovation_lab/jet/web/store/root.ts`
- `/Users/sarathfrancis/work/git/innovation_lab/jet/web/hooks/use-integration-popup.tsx`
- `/Users/sarathfrancis/work/git/innovation_lab/jet/web/lib/mobx/store-provider.tsx`
- `/Users/sarathfrancis/work/git/innovation_lab/jet/web/components/integration/` (all integration components)

---

