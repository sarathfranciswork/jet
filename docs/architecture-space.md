# Architecture - Space Application

**Generated:** 2026-03-18
**Part:** space
**Type:** Next.js Frontend (Public Sharing)

## Overview

Space is a lightweight Next.js application for publicly sharing Plane projects. It provides read-only access to published project boards with issue viewing, commenting, reactions, and voting — all without requiring authentication.

## Technology Stack

| Category | Technology | Version |
|----------|-----------|---------|
| Framework | Next.js | 12.3.2 |
| UI Library | React | 18.2.0 |
| Language | TypeScript | 4.7.4 |
| State Management | MobX | 6.10.0 |
| HTTP Client | Axios (via APIService) | - |
| Styling | Tailwind CSS | Custom config |
| Data Fetching | SWR | - |

## Key Differences from Web App

| Aspect | Web | Space |
|--------|-----|-------|
| Authentication | Required (JWT) | Optional (public endpoints) |
| API Endpoints | `/api/v1/...` | `/api/v1/public/...` |
| Capabilities | Full CRUD | Read + React/Vote/Comment |
| MobX Stores | 50+ stores | 4 stores |
| Components | 990+ files | ~50 files |
| Port | 3000 | 4000 |
| Base Path | `/` | `/spaces` (with Nginx) |

## Routing

```
/                               → Redirect to login
/login                          → Login view
/onboarding                     → User onboarding
/[workspace_slug]/              → Workspace index
/[workspace_slug]/[project_slug]/ → Public project board
/404                            → Not found
```

## State Management

4 MobX stores via RootStore:

| Store | State | Key Actions |
|-------|-------|-------------|
| UserStore | currentUser, loader, error | fetchCurrentUser() |
| ProjectStore | workspace, project, deploySettings, activeBoard, viewOptions | fetchProjectSettings(), setActiveBoard() |
| IssueStore | issues, states, labels, filteredStates/Labels/Priorities | fetchPublicIssues(), getFilteredIssuesByState() |
| IssueDetailStore | details, peekId, peekMode | fetchIssueDetails(), addIssueComment(), addIssueReaction(), addIssueVote() |

## Components

| Directory | Components | Purpose |
|-----------|-----------|---------|
| accounts/ | 8 | Authentication (sign-in, OAuth, password forms) |
| issues/navbar/ | 6 | Issue list navigation (filters, search, view selection) |
| issues/board-views/ | 5 dirs | List, Kanban, Calendar, Spreadsheet, Gantt views |
| issues/peek-overview/ | 12 | Issue detail modal (properties, comments, reactions, votes) |
| issues/filters-render/ | 3 dirs | State, priority, label filter blocks |
| views/ | 2 | Login view, project details view |
| ui/ | 10 | Button, input, loader, tooltip, dropdown, etc. |
| icons/ | Various | State group icons, custom SVGs |

## Services

| Service | Endpoints | Purpose |
|---------|----------|---------|
| APIService | Base class | Axios wrapper with auth |
| IssueService | Public issue endpoints | Fetch issues, votes, reactions, comments |
| UserService | `/api/users/me/` | Current user (optional) |
| ProjectService | Public project settings | Deploy board configuration |
| AuthenticationService | Auth endpoints | Login/signup |
| FileService | File upload | Asset management |

## Board Views

Space supports 5 issue display formats (same as web but read-only):
- **List** — Grouped by state, expandable rows
- **Kanban** — Columns by state/priority/label
- **Calendar** — Date-based grid
- **Spreadsheet** — Table with columns
- **Gantt** — Timeline visualization

## Peek Overview (Issue Detail)

Three peek modes:
- **Side** — Side panel overlay
- **Modal** — Centered modal
- **Full** — Full-screen view

Includes: issue properties, description, activity timeline, comments, reactions, votes.

## Configuration

- **`next.config.js`** — `basePath: "/spaces"` when `NEXT_PUBLIC_DEPLOY_WITH_NGINX=1`
- **`tailwind.config.js`** — Extends shared tailwind config
- **`tsconfig.json`** — Extends `tsconfig/nextjs.json`
