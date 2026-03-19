from django.urls import path


from jet.api.views import (
    IntegrationViewSet,
    WorkspaceIntegrationViewSet,
    GithubRepositoriesEndpoint,
    GithubRepositorySyncViewSet,
    GithubIssueSyncViewSet,
    GithubCommentSyncViewSet,
    BulkCreateGithubIssueSyncEndpoint,
    GithubSyncConfigViewSet,
    GithubUserMappingViewSet,
    GithubPullRequestViewSet,
    GithubSyncLogViewSet,
    SlackProjectSyncViewSet,
)


urlpatterns = [
    path(
        "integrations/",
        IntegrationViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="integrations",
    ),
    path(
        "integrations/<uuid:pk>/",
        IntegrationViewSet.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="integrations",
    ),
    path(
        "workspaces/<str:slug>/workspace-integrations/",
        WorkspaceIntegrationViewSet.as_view(
            {
                "get": "list",
            }
        ),
        name="workspace-integrations",
    ),
    path(
        "workspaces/<str:slug>/workspace-integrations/<str:provider>/",
        WorkspaceIntegrationViewSet.as_view(
            {
                "post": "create",
            }
        ),
        name="workspace-integrations",
    ),
    path(
        "workspaces/<str:slug>/workspace-integrations/<uuid:pk>/provider/",
        WorkspaceIntegrationViewSet.as_view(
            {
                "get": "retrieve",
                "delete": "destroy",
            }
        ),
        name="workspace-integrations",
    ),
    # Github Integrations
    path(
        "workspaces/<str:slug>/workspace-integrations/<uuid:workspace_integration_id>/github-repositories/",
        GithubRepositoriesEndpoint.as_view(),
    ),
    path(
        "workspaces/<str:slug>/projects/<uuid:project_id>/workspace-integrations/<uuid:workspace_integration_id>/github-repository-sync/",
        GithubRepositorySyncViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "workspaces/<str:slug>/projects/<uuid:project_id>/workspace-integrations/<uuid:workspace_integration_id>/github-repository-sync/<uuid:pk>/",
        GithubRepositorySyncViewSet.as_view(
            {
                "get": "retrieve",
                "delete": "destroy",
            }
        ),
    ),
    path(
        "workspaces/<str:slug>/projects/<uuid:project_id>/github-repository-sync/<uuid:repo_sync_id>/github-issue-sync/",
        GithubIssueSyncViewSet.as_view(
            {
                "post": "create",
                "get": "list",
            }
        ),
    ),
    path(
        "workspaces/<str:slug>/projects/<uuid:project_id>/github-repository-sync/<uuid:repo_sync_id>/bulk-create-github-issue-sync/",
        BulkCreateGithubIssueSyncEndpoint.as_view(),
    ),
    path(
        "workspaces/<str:slug>/projects/<uuid:project_id>/github-repository-sync/<uuid:repo_sync_id>/github-issue-sync/<uuid:pk>/",
        GithubIssueSyncViewSet.as_view(
            {
                "get": "retrieve",
                "delete": "destroy",
            }
        ),
    ),
    path(
        "workspaces/<str:slug>/projects/<uuid:project_id>/github-repository-sync/<uuid:repo_sync_id>/github-issue-sync/<uuid:issue_sync_id>/github-comment-sync/",
        GithubCommentSyncViewSet.as_view(
            {
                "post": "create",
                "get": "list",
            }
        ),
    ),
    path(
        "workspaces/<str:slug>/projects/<uuid:project_id>/github-repository-sync/<uuid:repo_sync_id>/github-issue-sync/<uuid:issue_sync_id>/github-comment-sync/<uuid:pk>/",
        GithubCommentSyncViewSet.as_view(
            {
                "get": "retrieve",
                "delete": "destroy",
            }
        ),
    ),
    # Github Sync Config
    path(
        "workspaces/<str:slug>/projects/<uuid:project_id>/github-repository-sync/<uuid:repo_sync_id>/sync-config/",
        GithubSyncConfigViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "workspaces/<str:slug>/projects/<uuid:project_id>/github-repository-sync/<uuid:repo_sync_id>/sync-config/<uuid:pk>/",
        GithubSyncConfigViewSet.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
    path(
        "workspaces/<str:slug>/projects/<uuid:project_id>/github-repository-sync/<uuid:repo_sync_id>/sync-config/<uuid:pk>/activate/",
        GithubSyncConfigViewSet.as_view({"post": "activate"}),
    ),
    path(
        "workspaces/<str:slug>/projects/<uuid:project_id>/github-repository-sync/<uuid:repo_sync_id>/sync-config/<uuid:pk>/deactivate/",
        GithubSyncConfigViewSet.as_view({"post": "deactivate"}),
    ),
    # Github User Mapping
    path(
        "workspaces/<str:slug>/github-user-mappings/",
        GithubUserMappingViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "workspaces/<str:slug>/github-user-mappings/<uuid:pk>/",
        GithubUserMappingViewSet.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
    # Github Pull Requests
    path(
        "workspaces/<str:slug>/projects/<uuid:project_id>/github-pull-requests/",
        GithubPullRequestViewSet.as_view(
            {
                "get": "list",
            }
        ),
    ),
    path(
        "workspaces/<str:slug>/projects/<uuid:project_id>/github-pull-requests/<uuid:pk>/",
        GithubPullRequestViewSet.as_view(
            {
                "get": "retrieve",
            }
        ),
    ),
    # Github Sync Logs
    path(
        "workspaces/<str:slug>/projects/<uuid:project_id>/github-sync-logs/",
        GithubSyncLogViewSet.as_view(
            {
                "get": "list",
            }
        ),
    ),
    ## End Github Integrations
    # Slack Integration
    path(
        "workspaces/<str:slug>/projects/<uuid:project_id>/workspace-integrations/<uuid:workspace_integration_id>/project-slack-sync/",
        SlackProjectSyncViewSet.as_view(
            {
                "post": "create",
                "get": "list",
            }
        ),
    ),
    path(
        "workspaces/<str:slug>/projects/<uuid:project_id>/workspace-integrations/<uuid:workspace_integration_id>/project-slack-sync/<uuid:pk>/",
        SlackProjectSyncViewSet.as_view(
            {
                "delete": "destroy",
                "get": "retrieve",
            }
        ),
    ),
    ## End Slack Integration
]
