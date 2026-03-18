# API Contracts - API Server

**Generated:** 2026-03-18
**Framework:** Django REST Framework 3.14.0
**Authentication:** JWT (simplejwt) — `Authorization: Bearer <token>`
**Base URL:** `{API_BASE_URL}/api/v1/`

## Authentication

All endpoints require `IsAuthenticated` unless marked `[AllowAny]`.

**JWT Tokens:**
- Access token lifetime: 7 days (10080 minutes)
- Refresh token lifetime: 43200 days
- Algorithm: HS256

---

## Authentication Endpoints

| Method | Path | View | Auth | Description |
|--------|------|------|------|-------------|
| POST | `/auth/sign-up/` | SignUpEndpoint | [AllowAny] | Register new user |
| POST | `/auth/sign-in/` | SignInEndpoint | [AllowAny] | Login with email/password |
| POST | `/auth/sign-out/` | SignOutEndpoint | Required | Logout |
| POST | `/auth/social-auth/` | OauthEndpoint | [AllowAny] | Google/GitHub OAuth |
| POST | `/auth/magic-generate/` | MagicSignInGenerateEndpoint | [AllowAny] | Generate magic link code |
| POST | `/auth/magic-sign-in/` | MagicSignInEndpoint | [AllowAny] | Verify magic link |
| POST | `/auth/token/refresh/` | TokenRefreshView | [AllowAny] | Refresh JWT token |
| GET | `/auth/email-verify/` | VerifyEmailEndpoint | Required | Verify email address |
| GET | `/auth/request-email-verify/` | RequestEmailVerificationEndpoint | Required | Request verification email |
| POST | `/auth/forgot-password/` | ForgotPasswordEndpoint | [AllowAny] | Request password reset |
| POST | `/auth/reset-password/<uidb64>/<token>/` | ResetPasswordEndpoint | [AllowAny] | Reset password |
| PATCH | `/auth/users/me/change-password/` | ChangePasswordEndpoint | Required | Change password |

---

## User Endpoints

| Method | Path | View | Permission | Description |
|--------|------|------|------------|-------------|
| GET | `/users/me/` | UserEndpoint | Authenticated | Get current user profile |
| PATCH | `/users/me/` | UserEndpoint | Authenticated | Update profile |
| GET | `/users/me/settings/` | UserEndpoint | Authenticated | Get user settings |
| PATCH | `/users/me/onboard/` | UpdateUserOnBoardedEndpoint | Authenticated | Mark onboarding complete |
| PATCH | `/users/me/tour-completed/` | UpdateUserTourCompletedEndpoint | Authenticated | Mark tour complete |

---

## Workspace Endpoints

| Method | Path | View | Permission | Description |
|--------|------|------|------------|-------------|
| GET | `/workspaces/` | WorkSpaceViewSet | Authenticated | List user workspaces |
| POST | `/workspaces/` | WorkSpaceViewSet | Authenticated | Create workspace |
| GET | `/workspaces/<slug>/` | WorkSpaceViewSet | WS Member | Get workspace details |
| PUT/PATCH | `/workspaces/<slug>/` | WorkSpaceViewSet | WS Admin/Owner | Update workspace |
| DELETE | `/workspaces/<slug>/` | WorkSpaceViewSet | WS Owner | Delete workspace |
| GET | `/workspaces/slug-check/` | WorkSpaceAvailabilityCheckEndpoint | Authenticated | Check slug availability |
| POST | `/workspaces/<slug>/invite/` | InviteWorkspaceEndpoint | WS Admin/Owner | Invite members |
| GET | `/workspaces/<slug>/invitations/` | WorkspaceInvitationsViewset | WS Admin/Owner | List pending invitations |
| GET | `/workspaces/<slug>/members/` | WorkSpaceMemberViewSet | WS Member | List members |
| GET | `/workspaces/<slug>/members/me/` | WorkspaceMemberUserEndpoint | WS Member | Get own membership |
| PATCH | `/workspaces/<slug>/members/<uuid>/` | WorkSpaceMemberViewSet | WS Admin/Owner | Update member role |
| DELETE | `/workspaces/<slug>/members/<uuid>/` | WorkSpaceMemberViewSet | WS Admin/Owner | Remove member |
| POST | `/workspaces/<slug>/leave/` | LeaveWorkspaceEndpoint | WS Member | Leave workspace |
| GET | `/workspaces/<slug>/labels/` | WorkspaceLabelsEndpoint | WS Member | List workspace labels |
| CRUD | `/workspaces/<slug>/themes/` | WorkspaceThemeViewSet | WS Member | Manage themes |
| GET | `/workspaces/<slug>/user-profile/<uuid>/` | WorkspaceUserProfileEndpoint | WS Member | View member profile |
| GET | `/workspaces/<slug>/user-profile/<uuid>/stats/` | WorkspaceUserProfileStatsEndpoint | WS Member | Member stats |
| GET | `/workspaces/<slug>/user-profile/<uuid>/activity/` | WorkspaceUserActivityEndpoint | WS Member | Member activity |
| GET | `/workspaces/<slug>/user-profile/<uuid>/issues/` | WorkspaceUserProfileIssuesEndpoint | WS Member | Member issues |

---

## Project Endpoints

| Method | Path | View | Permission | Description |
|--------|------|------|------------|-------------|
| GET | `/workspaces/<slug>/projects/` | ProjectViewSet | WS Member | List projects |
| POST | `/workspaces/<slug>/projects/` | ProjectViewSet | WS Admin/Member | Create project |
| GET | `/workspaces/<slug>/projects/<uuid>/` | ProjectViewSet | Project Member | Get project details |
| PUT/PATCH | `/workspaces/<slug>/projects/<uuid>/` | ProjectViewSet | Project Admin | Update project |
| DELETE | `/workspaces/<slug>/projects/<uuid>/` | ProjectViewSet | Project Admin | Delete project |
| GET | `/workspaces/<slug>/project-identifiers/` | ProjectIdentifierEndpoint | WS Member | List identifiers |
| POST | `/workspaces/<slug>/projects/<uuid>/invite/` | InviteProjectEndpoint | Project Admin | Invite to project |
| GET | `/workspaces/<slug>/projects/<uuid>/members/` | ProjectMemberViewSet | Project Member | List members |
| PATCH | `/workspaces/<slug>/projects/<uuid>/members/<uuid>/` | ProjectMemberViewSet | Project Admin | Update member role |
| DELETE | `/workspaces/<slug>/projects/<uuid>/members/<uuid>/` | ProjectMemberViewSet | Project Admin | Remove member |
| POST | `/workspaces/<slug>/projects/join/` | ProjectJoinEndpoint | WS Member | Join public project |
| POST | `/workspaces/<slug>/projects/<uuid>/team-invite/` | AddTeamToProjectEndpoint | Project Admin | Add team |
| GET | `/workspaces/<slug>/projects/<uuid>/invitations/` | ProjectMemberInvitationsViewset | Project Admin | List invitations |
| CRUD | `/workspaces/<slug>/projects/<uuid>/favorites/` | ProjectFavoritesViewSet | Project Member | Manage favorites |

---

## Issue Endpoints

| Method | Path | View | Permission | Description |
|--------|------|------|------------|-------------|
| GET | `/workspaces/<slug>/projects/<uuid>/issues/` | IssueViewSet | Project Member | List issues (filterable) |
| POST | `/workspaces/<slug>/projects/<uuid>/issues/` | IssueViewSet | Project Admin/Member | Create issue |
| GET | `/workspaces/<slug>/projects/<uuid>/issues/<uuid>/` | IssueViewSet | Project Member | Get issue detail |
| PUT/PATCH | `/workspaces/<slug>/projects/<uuid>/issues/<uuid>/` | IssueViewSet | Project Admin/Member | Update issue |
| DELETE | `/workspaces/<slug>/projects/<uuid>/issues/<uuid>/` | IssueViewSet | Project Admin/Member | Delete issue |
| GET | `/workspaces/<slug>/my-issues/` | UserWorkSpaceIssues | WS Member | User's assigned issues |
| POST | `/workspaces/<slug>/projects/<uuid>/issues/<uuid>/sub-issues/` | SubIssuesEndpoint | Project Member | Add sub-issues |
| CRUD | `/workspaces/<slug>/projects/<uuid>/issues/<uuid>/issue-links/` | IssueLinkViewSet | Project Member | Manage links |
| CRUD | `/workspaces/<slug>/projects/<uuid>/issues/<uuid>/comments/` | IssueCommentViewSet | Project Member | Manage comments |
| CRUD | `/workspaces/<slug>/projects/<uuid>/issues/<uuid>/subscribers/` | IssueSubscriberViewSet | Project Member | Manage subscribers |
| CRUD | `/workspaces/<slug>/projects/<uuid>/issues/<uuid>/reactions/` | IssueReactionViewSet | Project Member | Manage reactions |
| CRUD | `/workspaces/<slug>/projects/<uuid>/comments/<uuid>/reactions/` | CommentReactionViewSet | Project Member | Comment reactions |
| GET | `/workspaces/<slug>/projects/<uuid>/issues/<uuid>/activity/` | IssueActivityEndpoint | Project Member | Issue activity log |
| CRUD | `/workspaces/<slug>/projects/<uuid>/issue-labels/` | LabelViewSet | Project Member | Manage labels |
| CRUD | `/workspaces/<slug>/projects/<uuid>/issue-relations/` | IssueRelationViewSet | Project Member | Issue relations |
| POST | `/workspaces/<slug>/projects/<uuid>/bulk-delete-issues/` | BulkDeleteIssuesEndpoint | Project Admin | Bulk delete |
| POST | `/workspaces/<slug>/projects/<uuid>/bulk-create-labels/` | BulkCreateIssueLabelsEndpoint | Project Admin | Bulk create labels |
| POST | `/workspaces/<slug>/projects/<uuid>/export-issues/` | ExportIssuesEndpoint | Project Member | Export issues |
| GET | `/workspaces/<slug>/projects/<uuid>/archived-issues/` | IssueArchiveViewSet | Project Member | List archived |
| CRUD | `/workspaces/<slug>/projects/<uuid>/draft-issues/` | IssueDraftViewSet | Project Member | Manage drafts |

---

## Cycle (Sprint) Endpoints

| Method | Path | View | Permission | Description |
|--------|------|------|------------|-------------|
| GET/POST | `/workspaces/<slug>/projects/<uuid>/cycles/` | CycleViewSet | Project Member | List/create cycles |
| GET/PUT/PATCH/DELETE | `/workspaces/<slug>/projects/<uuid>/cycles/<uuid>/` | CycleViewSet | Project Member | Cycle CRUD |
| GET/POST | `/workspaces/<slug>/projects/<uuid>/cycles/<uuid>/cycle-issues/` | CycleIssueViewSet | Project Member | Manage cycle issues |
| DELETE | `/workspaces/<slug>/projects/<uuid>/cycles/<uuid>/cycle-issues/<uuid>/` | CycleIssueViewSet | Project Member | Remove from cycle |
| POST | `/workspaces/<slug>/projects/<uuid>/cycles/<uuid>/date-check/` | CycleDateCheckEndpoint | Project Member | Validate dates |
| POST | `/workspaces/<slug>/projects/<uuid>/cycles/<uuid>/transfer-issues/` | TransferCycleIssueEndpoint | Project Member | Transfer issues |
| CRUD | `/workspaces/<slug>/projects/<uuid>/user-favorite-cycles/` | CycleFavoriteViewSet | Project Member | Favorite cycles |

---

## Module Endpoints

| Method | Path | View | Permission | Description |
|--------|------|------|------------|-------------|
| GET/POST | `/workspaces/<slug>/projects/<uuid>/modules/` | ModuleViewSet | Project Member | List/create modules |
| GET/PATCH/DELETE | `/workspaces/<slug>/projects/<uuid>/modules/<uuid>/` | ModuleViewSet | Project Member | Module CRUD |
| GET/POST | `/workspaces/<slug>/projects/<uuid>/modules/<uuid>/module-issues/` | ModuleIssueViewSet | Project Member | Manage module issues |
| CRUD | `/workspaces/<slug>/projects/<uuid>/modules/<uuid>/module-links/` | ModuleLinkViewSet | Project Member | Module links |
| CRUD | `/workspaces/<slug>/projects/<uuid>/user-favorite-modules/` | ModuleFavoriteViewSet | Project Member | Favorite modules |

---

## State Endpoints

| Method | Path | View | Permission | Description |
|--------|------|------|------------|-------------|
| GET/POST | `/workspaces/<slug>/projects/<uuid>/states/` | StateViewSet | Project Member | List/create states |
| GET/PUT/PATCH/DELETE | `/workspaces/<slug>/projects/<uuid>/states/<uuid>/` | StateViewSet | Project Admin | State CRUD |

---

## View Endpoints

| Method | Path | View | Permission | Description |
|--------|------|------|------------|-------------|
| GET/POST | `/workspaces/<slug>/projects/<uuid>/views/` | IssueViewViewSet | Project Member | List/create views |
| GET/PATCH/DELETE | `/workspaces/<slug>/projects/<uuid>/views/<uuid>/` | IssueViewViewSet | Project Member | View CRUD |
| CRUD | `/workspaces/<slug>/projects/<uuid>/user-favorite-views/` | IssueViewFavoriteViewSet | Project Member | Favorite views |
| CRUD | `/workspaces/<slug>/views/` | GlobalViewViewSet | WS Member | Global views |

---

## Page Endpoints

| Method | Path | View | Permission | Description |
|--------|------|------|------------|-------------|
| GET/POST | `/workspaces/<slug>/projects/<uuid>/pages/` | PageViewSet | Project Member | List/create pages |
| GET/PATCH/DELETE | `/workspaces/<slug>/projects/<uuid>/pages/<uuid>/` | PageViewSet | Project Member | Page CRUD |
| CRUD | `/workspaces/<slug>/projects/<uuid>/pages/<uuid>/page-blocks/` | PageBlockViewSet | Project Member | Page blocks |
| CRUD | `/workspaces/<slug>/projects/<uuid>/user-favorite-pages/` | PageFavoriteViewSet | Project Member | Favorite pages |

---

## Inbox Endpoints

| Method | Path | View | Permission | Description |
|--------|------|------|------------|-------------|
| GET/POST | `/workspaces/<slug>/projects/<uuid>/inboxes/` | InboxViewSet | Project Member | List/create inboxes |
| CRUD | `/workspaces/<slug>/projects/<uuid>/inboxes/<uuid>/inbox-issues/` | InboxIssueViewSet | Project Member | Manage inbox issues |

---

## Estimate Endpoints

| Method | Path | View | Permission | Description |
|--------|------|------|------------|-------------|
| GET | `/workspaces/<slug>/projects/<uuid>/estimates/` | ProjectEstimatePointEndpoint | Project Member | List estimates |
| PATCH | `/workspaces/<slug>/projects/<uuid>/estimates/` | BulkEstimatePointEndpoint | Project Admin | Bulk update points |

---

## Notification Endpoints

| Method | Path | View | Permission | Description |
|--------|------|------|------------|-------------|
| GET | `/workspaces/<slug>/users/notifications/` | NotificationViewSet | WS Member | List notifications |
| PATCH | `/workspaces/<slug>/users/notifications/<uuid>/` | NotificationViewSet | WS Member | Update notification |
| POST | `/workspaces/<slug>/users/notifications/<uuid>/read/` | NotificationViewSet | WS Member | Mark as read |
| POST | `/workspaces/<slug>/users/notifications/<uuid>/archive/` | NotificationViewSet | WS Member | Archive notification |

---

## Asset/Upload Endpoints

| Method | Path | View | Permission | Description |
|--------|------|------|------------|-------------|
| POST | `/users/file-assets/` | FileAssetEndpoint | Authenticated | Upload file |
| GET/DELETE | `/users/file-assets/<uuid>/` | FileAssetEndpoint | Authenticated | Get/delete asset |
| GET | `/workspaces/<slug>/user-assets/` | UserAssetsEndpoint | WS Member | User file assets |

---

## Analytics Endpoints

| Method | Path | View | Permission | Description |
|--------|------|------|------------|-------------|
| GET | `/workspaces/<slug>/analytics/` | AnalyticsEndpoint | WS Member | Run analytics query |
| GET | `/workspaces/<slug>/analytics/default/` | DefaultAnalyticsEndpoint | WS Member | Default analytics |
| POST | `/workspaces/<slug>/analytics/export/` | ExportAnalyticsEndpoint | WS Member | Export analytics |
| CRUD | `/workspaces/<slug>/analytic-views/` | AnalyticViewViewset | WS Member | Saved analytic views |

---

## Integration Endpoints

| Method | Path | View | Permission | Description |
|--------|------|------|------------|-------------|
| GET | `/workspaces/<slug>/integrations/` | WorkspaceIntegrationViewSet | WS Admin | List integrations |
| POST | `/workspaces/<slug>/projects/<uuid>/github-repositories/` | GithubRepositoriesEndpoint | Project Admin | Link GitHub repos |
| CRUD | `/workspaces/<slug>/projects/<uuid>/github-repository-syncs/` | GithubRepositorySyncViewSet | Project Admin | GitHub sync config |
| CRUD | `/workspaces/<slug>/projects/<uuid>/github-issue-syncs/` | GithubIssueSyncViewSet | Project Admin | Issue sync mapping |
| CRUD | `/workspaces/<slug>/projects/<uuid>/slack-project-syncs/` | SlackProjectSyncViewSet | Project Admin | Slack sync config |

---

## Import/Export Endpoints

| Method | Path | View | Permission | Description |
|--------|------|------|------------|-------------|
| POST | `/workspaces/<slug>/importers/` | ImportServiceEndpoint | WS Admin | Start import (GitHub/Jira) |
| GET | `/workspaces/<slug>/importers/<uuid>/` | ServiceIssueImportSummaryEndpoint | WS Admin | Import summary |
| POST | `/workspaces/<slug>/importers/<uuid>/` | UpdateServiceImportStatusEndpoint | WS Admin | Update import status |

---

## Search Endpoints

| Method | Path | View | Permission | Description |
|--------|------|------|------------|-------------|
| GET | `/workspaces/<slug>/search/` | GlobalSearchEndpoint | WS Member | Full-text search |

---

## External Service Endpoints

| Method | Path | View | Permission | Description |
|--------|------|------|------------|-------------|
| POST | `/workspaces/<slug>/projects/<uuid>/ai-assistant/` | GPTIntegrationEndpoint | Project Member | AI-powered assistance |
| GET | `/unsplash/` | UnsplashEndpoint | [AllowAny] | Search Unsplash images |
| GET | `/release-notes/` | ReleaseNotesEndpoint | [AllowAny] | GitHub release notes |

---

## Configuration Endpoints

| Method | Path | View | Permission | Description |
|--------|------|------|------------|-------------|
| GET | `/configs/` | ConfigurationEndpoint | [AllowAny] | App configuration |

---

## Public Board Endpoints

These endpoints serve the **Space** (public sharing) app and require no authentication:

| Method | Path | View | Auth | Description |
|--------|------|------|------|-------------|
| GET | `/public/workspaces/<slug>/project-boards/<uuid>/settings/` | ProjectDeployBoardPublicSettingsEndpoint | [AllowAny] | Public project settings |
| GET | `/public/workspaces/<slug>/project-boards/<uuid>/issues/` | ProjectIssuesPublicEndpoint | [AllowAny] | List public issues |
| GET | `/public/workspaces/<slug>/project-boards/<uuid>/issues/<uuid>/` | IssueDetailPublicEndpoint | [AllowAny] | Issue detail |
| GET/POST | `/public/workspaces/<slug>/project-boards/<uuid>/issues/<uuid>/comments/` | IssueCommentPublicEndpoint | [AllowAny] | Issue comments |
| GET/POST | `/public/workspaces/<slug>/project-boards/<uuid>/issues/<uuid>/reactions/` | IssueReactionPublicEndpoint | [AllowAny] | Issue reactions |
| GET/POST/DELETE | `/public/workspaces/<slug>/project-boards/<uuid>/issues/<uuid>/votes/` | IssueVotePublicEndpoint | [AllowAny] | Issue votes |

---

## Permission Summary

| Level | Role | Value | Capabilities |
|-------|------|-------|-------------|
| Workspace | Owner | 20 | Full control, delete workspace |
| Workspace | Admin | 15 | Manage members, settings |
| Workspace | Member | 10 | Read, create projects |
| Workspace | Guest | 5 | Read-only |
| Project | Admin | 20 | Full project control |
| Project | Member | 15 | Create/edit issues |
| Project | Viewer | 10 | Read-only |
| Project | Guest | 5 | Limited read |

## Error Response Format

```json
{
  "error": "Error message description"
}
```

HTTP status codes follow REST conventions: 200 (OK), 201 (Created), 204 (No Content), 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), 500 (Server Error).
