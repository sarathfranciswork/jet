# Component Inventory - Web Application

**Generated:** 2026-03-18
**Total Components:** ~990 TypeScript/TSX files across 35 directories

## Component Categories

### Issues (200+ components) — `components/issues/`

The largest component group, handling all issue-related UI.

#### Issue Layouts — `issue-layouts/`
Multi-layout rendering system supporting 5 view modes:

| Layout | Directory | Key Components |
|--------|-----------|---------------|
| List | `list/` | ListLayout, ListBlock, ListInlineCreate |
| Kanban | `kanban/` | KanbanLayout, KanbanBlock, KanbanGroup, swimlanes |
| Calendar | `calendar/` | CalendarLayout, CalendarDayTile, CalendarWeekHeader |
| Spreadsheet | `spreadsheet/` | SpreadsheetLayout, SpreadsheetView, SpreadsheetColumns |
| Gantt | `gantt/` | GanttLayout, GanttBlock, GanttSidebar |

Shared: `root.tsx` (layout switcher), `AppliedFilters`, `FilterSelection`, `DisplayFilters`

#### Issue Peek Overview — `issue-peek-overview/`
Quick issue preview without navigation:
- `layout.tsx` — Peek container (side/modal/full modes)
- `header.tsx` — Peek header with actions
- `activity.tsx` — Activity timeline
- `properties.tsx` — Issue property sidebar
- `issue-detail.tsx` — Main content area

#### Sidebar Select — `sidebar-select/`
Issue property selectors:
- State, Priority, Assignee, Label, Cycle, Module
- Start date, Due date, Estimate, Parent issue, Relation

#### Other Issue Components
- `form.tsx` — Issue creation/edit form
- `modal.tsx` — Issue modal wrapper
- `description-form.tsx` — Rich description editor
- `activity.tsx` — Activity timeline
- `comment/` — Comment threads
- `attachment/` — File attachments
- `sub-issues/` — Sub-issue management
- `select/` — Selection dropdowns

### Headers (25 components) — `components/headers/`

One header per page type, providing breadcrumbs, filters, and actions:

| Header | Route | Features |
|--------|-------|----------|
| project-issues | Issues list | Layout selection, filters, analytics modal |
| cycle-issues | Cycle detail | Cycle info, filters, layout |
| module-issues | Module detail | Module info, filters |
| project-views | Views list | Create view button |
| project-view-issues | View detail | View filters |
| pages | Pages list | Sort options |
| page-details | Page detail | Page actions |
| workspace-dashboard | Dashboard | Date range, greeting |
| workspace-analytics | Analytics | Analytics controls |
| global-issues | Global view | Cross-project filters |
| project-settings | Settings | Settings nav |
| workspace-settings | WS settings | Settings nav |
| profile-preferences | Profile | Preferences nav |
| project-archived-issues | Archive | Archive filters |
| project-draft-issues | Drafts | Draft filters |
| project-inbox | Inbox | Inbox filters |

### Workspace (20+ components) — `components/workspace/`

| Component | Purpose |
|-----------|---------|
| sidebar-dropdown | Workspace switcher in sidebar |
| sidebar-menu | Main navigation menu |
| sidebar-quick-action | Quick action buttons |
| create-workspace-form | New workspace form |
| send-workspace-invitation-modal | Invite members dialog |
| member-select | Member picker |
| delete-workspace-modal | Deletion confirmation |
| confirm-workspace-member-remove | Member removal dialog |
| issues-list | Quick issue list widget |
| issues-stats | Statistics cards |
| completed-issues-graph | Activity graph visualization |
| settings/ | Members, billing, general settings |

### Project (24+ components) — `components/project/`

| Component | Purpose |
|-----------|---------|
| create-project-modal | New project form (name, identifier, emoji, icon) |
| form | Project settings form |
| card, card-list | Project card display |
| sidebar-list, sidebar-list-item | Sidebar project navigation |
| member-list, member-list-item | Project members management |
| delete-project-modal | Deletion confirmation |
| leave-project-modal | Leave project dialog |
| join-project-modal | Join project dialog |
| send-project-invitation-modal | Invite members |
| publish-project/ | Public project publishing |
| settings/ | States, labels, estimates, members, automations |

### Cycles (20 components) — `components/cycles/`

| Component | Purpose |
|-----------|---------|
| active-cycle-details | Active cycle summary card |
| cycles-list | Cycle listing |
| cycle-create-edit-modal | Create/edit cycle form |
| delete-cycle-modal | Deletion confirmation |
| sidebar | Cycle detail sidebar |
| form | Cycle form fields |
| gantt-chart | Cycle Gantt visualization |
| transfer-issues-modal | Transfer issues between cycles |
| select | Cycle selector dropdown |

### Modules (14 components) — `components/modules/`

| Component | Purpose |
|-----------|---------|
| modules-list-view | Module listing |
| module-create-edit-modal | Create/edit module |
| delete-module-modal | Deletion confirmation |
| sidebar | Module detail sidebar |
| form | Module form fields |
| gantt-chart | Module Gantt visualization |
| select-member | Module member selection |

### UI Primitives (27 components) — `components/ui/`

| Component | Purpose |
|-----------|---------|
| dropdowns/ | CustomMenu, Select, SearchSelect, ContextMenu |
| input/ | Text input with validation |
| text-area/ | Multi-line textarea |
| datepicker | Date/range picker (react-datepicker) |
| date | Date display formatter |
| tooltip | Hover tooltip |
| toggle-switch | Boolean toggle |
| circular-progress | Progress circle |
| progress-bar | Linear progress bar |
| linear-progress-indicator | Multi-segment progress |
| loader, spinner | Loading indicators |
| empty-space | Empty state placeholder |
| labels-list | Label chips display |
| icon | Icon wrapper |
| markdown-to-component | Markdown renderer |
| multi-level-dropdown | Nested menu |
| product-updates-modal | Changelog modal |
| graphs/ | Nivo chart wrappers (bar, line, pie) |

### Core (10+ components) — `components/core/`

| Component | Purpose |
|-----------|---------|
| activity | Activity stream |
| modals/ | Confirmation dialogs, custom modals |
| filters/ | Advanced filter UI components |
| theme/ | Theme customization panel |
| sidebar/ | Settings sidebar navigation |
| image-picker-popover | Image selection from Unsplash |
| reaction-selector | Emoji reaction picker |

### Command Palette (9 components) — `components/command-palette/`

| Component | Purpose |
|-----------|---------|
| command-palette | Main command menu (Cmd+K) |
| command-k | Keyboard shortcut handler |
| shortcuts-modal | Shortcuts reference |
| change-interface-theme | Theme quick switcher |
| actions/ | Create issue, navigate, search |

### Analytics — `components/analytics/`

| Component | Purpose |
|-----------|---------|
| analytics-modal | Analytics overlay |
| custom-analytics | Custom query builder |
| scope-and-demand | Scope vs demand charts |
| project-modal | Project-specific analytics |

### Gantt Chart (15 components) — `components/gantt-chart/`

| Component | Purpose |
|-----------|---------|
| chart | Main chart container |
| blocks | Timeline blocks |
| sidebar | Gantt sidebar with issue list |
| views/ | Day, week, month, quarter views |
| helpers/ | Date calculations, positioning |

### Pages (13 components) — `components/pages/`

| Component | Purpose |
|-----------|---------|
| pages-list | Page listing with grid/list toggle |
| page-form | Page create/edit form |
| create-update-page-modal | Page modal |
| delete-page-modal | Deletion confirmation |
| single-page-block | Page block component |
| single-page-detailed-item | Detailed page list item |

### Views (9 components) — `components/views/`

| Component | Purpose |
|-----------|---------|
| views-list | View listing |
| modal | Create/edit view dialog |
| delete-view-modal | Deletion confirmation |
| form | View configuration form |

### Icons (91 components) — `components/icons/`

Custom SVG icon components organized by category:
- State group icons (backlog, unstarted, started, completed, cancelled)
- Priority icons (urgent, high, medium, low, none)
- Cycle icons
- Module icons
- General UI icons (archive, clipboard, discord, github, attach, etc.)

### Other Component Groups

| Directory | Count | Purpose |
|-----------|-------|---------|
| notifications/ | 7 | Notification panel, items, settings |
| labels/ | 11 | Label management, color picker, hierarchy |
| states/ | 9 | State management, color selection |
| breadcrumbs/ | 3 | Navigation breadcrumbs |
| emoji-icon-picker/ | 4 | Emoji/icon selection |
| integration/ | 10 | GitHub, Slack integration UI |
| profile/ | 5 | User profile components |
| exporter/ | 3 | Data export UI |
| onboarding/ | 5 | Onboarding flow steps |
| dnd/ | 2 | Drag-and-drop utilities |
| auth-screens/ | 6 | Authentication forms |
| account/ | 3 | Account settings |
| toast-alert/ | 1 | Toast notification |
| automation/ | 3 | Archive/close automation rules |
| common/ | 2 | Common utilities |
