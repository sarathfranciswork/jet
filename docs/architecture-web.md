# Architecture - Web Application

**Generated:** 2026-03-18
**Part:** web
**Type:** Next.js Frontend Application

## Overview

The web application is the main Plane dashboard — a Next.js 12.3.2 application using React 18, TypeScript, MobX for state management, and Tailwind CSS for styling. It serves as the primary interface for project management, issue tracking, sprint planning, and analytics.

## Technology Stack

| Category | Technology | Version |
|----------|-----------|---------|
| Framework | Next.js | 12.3.2 |
| UI Library | React | 18.2.0 |
| Language | TypeScript | 4.7.4 |
| State Management | MobX + mobx-react-lite | 6.10.0 |
| Data Fetching | SWR | 2.1.3 |
| HTTP Client | Axios | 1.1.3 |
| Styling | Tailwind CSS | 3.3.3 |
| Forms | React Hook Form | 7.38.0 |
| UI Components | @plane/ui, Blueprint.js, Headless UI, MUI | Various |
| Rich Text | @plane/rich-text-editor, @plane/lite-text-editor | Custom |
| Charts | Nivo (@nivo/bar, line, pie) | 0.80.0 |
| Icons | Lucide React + 91 custom SVGs | 0.274.0 |
| Drag & Drop | @hello-pangea/dnd | 16.3.0 |
| Command Menu | cmdk | 0.2.0 |
| Theme | next-themes | 0.2.1 |
| Monitoring | Sentry (@sentry/nextjs) | 7.36.0 |

## Architecture Pattern

**Component-based MVC with MobX reactive stores**

```
Pages (Routes) → Layouts → Components → Stores → Services → API
                                          ↑
                                        Hooks
                                        Contexts
                                        Helpers
```

## Routing Structure

Next.js file-based routing with nested dynamic segments:

```
/                                    → Sign-in
/accounts/sign-in                    → Email/password login
/accounts/sign-up                    → Registration
/accounts/magic-sign-in              → Magic link
/create-workspace                    → New workspace
/onboarding                         → User onboarding
/[workspaceSlug]/                    → Workspace dashboard
/[workspaceSlug]/settings/           → Workspace settings
/[workspaceSlug]/projects/           → Project listing
/[workspaceSlug]/profile/            → User profile
/[workspaceSlug]/projects/[projectId]/issues/          → Issues (all layouts)
/[workspaceSlug]/projects/[projectId]/cycles/           → Cycles/sprints
/[workspaceSlug]/projects/[projectId]/modules/          → Modules
/[workspaceSlug]/projects/[projectId]/views/             → Custom views
/[workspaceSlug]/projects/[projectId]/pages/             → Wiki pages
/[workspaceSlug]/projects/[projectId]/inbox/             → Inbox triage
/[workspaceSlug]/projects/[projectId]/settings/          → Project settings
/[workspaceSlug]/projects/[projectId]/archived-issues/   → Archived issues
/[workspaceSlug]/projects/[projectId]/draft-issues/      → Draft issues
```

## State Management (MobX)

Central `RootStore` in `store/root.ts` aggregates 50+ sub-stores:

### Store Categories

| Category | Stores | Purpose |
|----------|--------|---------|
| Core | user, theme, commandPalette | Auth, UI state |
| Workspace | workspace, workspaceFilter | Workspace data, filtering |
| Project | project, projectState, projectLabel, projectEstimates, projectPublish | Project config |
| Issues | issue, issueFilter, issueDetail, issueKanBanView, issueCalendarView, quickAddIssue, draftIssuesStore | Issue CRUD & display |
| Cycles | cycle, cycleIssue, cycleIssueFilter, cycleIssueKanBanView, cycleIssueCalendarView | Sprint management |
| Modules | module, moduleIssue, moduleFilter, moduleIssueKanBanView, moduleIssueCalendarView | Feature modules |
| Views | projectViews, projectViewIssues, projectViewFilters, projectViewIssueCalendarView | Custom views |
| Global Views | globalViews, globalViewIssues, globalViewFilters | Cross-project views |
| Other | calendar, profileIssues, archivedIssues, draftIssues, inbox (4 stores), mentionsStore | Specialized |

### Store Pattern
```typescript
// Each store follows this pattern:
class ExampleStore implements IExampleStore {
  // Observable state
  items: Map<string, IItem> = new Map()
  loading: boolean = false

  // Root store reference
  rootStore: RootStore

  constructor(rootStore: RootStore) {
    makeObservable(this, { items: observable, loading: observable, ... })
    this.rootStore = rootStore
  }

  // Actions (API calls + state updates)
  fetchItems = async (params) => { ... }
  createItem = async (data) => { ... }
  updateItem = async (id, data) => { ... }
  deleteItem = async (id) => { ... }

  // Computed values
  get sortedItems() { ... }
}
```

## Service Layer

21+ service classes extending `APIService` base:

```typescript
abstract class APIService {
  protected baseURL: string  // NEXT_PUBLIC_API_BASE_URL

  // Cookie-based JWT auth
  setAccessToken(token), getAccessToken()
  setRefreshToken(token), getRefreshToken()

  // HTTP methods (axios)
  get(url, config?), post(url, data?, config?)
  put(url, data?, config?), patch(url, data?, config?)
  delete(url, data?, config?), request(config?)
}
```

| Service | API Scope |
|---------|----------|
| AuthService | Authentication (sign-in, sign-up, OAuth, magic link) |
| UserService | User profile, settings, onboarding |
| WorkspaceService | Workspace CRUD, members, invitations |
| ProjectService | Project CRUD, members, favorites |
| IssueService | Issue CRUD, comments, attachments, reactions |
| CycleService | Cycle CRUD, issue assignment |
| ModuleService | Module CRUD, issue assignment |
| PageService | Page CRUD, page blocks |
| ViewService | Custom view CRUD |
| InboxService | Inbox management |
| NotificationService | Notification management |
| AnalyticsService | Analytics queries |
| FileService | File uploads/downloads |
| AIService | OpenAI GPT integration |

## Layout System

```
DefaultLayout        → Full-screen (auth pages, error pages)
AppLayout            → Sidebar + Header + Content
  ├── UserAuthWrapper      → Redirect if not logged in
  ├── WorkspaceAuthWrapper → Validate workspace access
  ├── ProjectAuthWrapper   → Validate project access (optional)
  └── CommandPalette       → Always available
SettingsLayout       → Settings sidebar + content
ProfileLayout        → Profile header + content
```

## Multi-Layout Issue Display

Issues support 5 view layouts, each with dedicated components and stores:

| Layout | Components | Store |
|--------|-----------|-------|
| List | `issue-layouts/list/` | issueStore |
| Kanban | `issue-layouts/kanban/` | issueKanBanViewStore |
| Calendar | `issue-layouts/calendar/` | issueCalendarViewStore |
| Spreadsheet | `issue-layouts/spreadsheet/` | issueStore |
| Gantt Chart | `issue-layouts/gantt/` | issueStore |

Filters, grouping, and sorting are shared across layouts via `issueFilterStore`.

## Theme System

5 themes: `light`, `dark`, `light-contrast`, `dark-contrast`, `custom`

- CSS variables define color scheme (18 primary shades, background/text/border/shadow levels)
- Sidebar has separate color variables
- Custom theme allows user-defined color palette
- Persisted via `next-themes` + localStorage
- Applied via `helpers/theme.helper.ts`

## Key Patterns

- **Optimistic Updates:** Issues use `tempId` for immediate UI updates before API response
- **SWR Caching:** All API calls cached with keys from `constants/fetch-keys.ts`
- **Filter Persistence:** Filters stored in URL params + localStorage for shareability
- **Peek Overview:** Side panel for quick issue inspection without navigation
- **Command Palette:** `Cmd+K` for keyboard-driven navigation and actions
- **Drag & Drop:** @hello-pangea/dnd for Kanban card reordering

## Component Count

| Directory | Files | Purpose |
|-----------|-------|---------|
| components/issues/ | 200+ | Issue management (largest group) |
| components/headers/ | 25 | Page headers |
| components/workspace/ | 20+ | Workspace UI |
| components/project/ | 24+ | Project UI |
| components/cycles/ | 20 | Cycle management |
| components/modules/ | 14 | Module management |
| components/ui/ | 27 | Shared UI primitives |
| components/icons/ | 91 | Custom SVG icons |
| **Total** | **~990** | |
