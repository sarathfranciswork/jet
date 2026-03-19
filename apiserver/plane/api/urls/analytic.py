from django.urls import path


from plane.api.views import (
    AnalyticsEndpoint,
    AnalyticViewViewset,
    SavedAnalyticEndpoint,
    ExportAnalyticsEndpoint,
    DefaultAnalyticsEndpoint,
    ProjectBurndownAnalyticsEndpoint,
    ProjectVelocityAnalyticsEndpoint,
    ProjectFlowAnalyticsEndpoint,
    ProjectWorkloadAnalyticsEndpoint,
)


urlpatterns = [
    path(
        "workspaces/<str:slug>/analytics/",
        AnalyticsEndpoint.as_view(),
        name="plane-analytics",
    ),
    path(
        "workspaces/<str:slug>/analytic-view/",
        AnalyticViewViewset.as_view({"get": "list", "post": "create"}),
        name="analytic-view",
    ),
    path(
        "workspaces/<str:slug>/analytic-view/<uuid:pk>/",
        AnalyticViewViewset.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
        name="analytic-view",
    ),
    path(
        "workspaces/<str:slug>/saved-analytic-view/<uuid:analytic_id>/",
        SavedAnalyticEndpoint.as_view(),
        name="saved-analytic-view",
    ),
    path(
        "workspaces/<str:slug>/export-analytics/",
        ExportAnalyticsEndpoint.as_view(),
        name="export-analytics",
    ),
    path(
        "workspaces/<str:slug>/default-analytics/",
        DefaultAnalyticsEndpoint.as_view(),
        name="default-analytics",
    ),
    # Project-level analytics
    path(
        "workspaces/<str:slug>/projects/<uuid:project_id>/analytics/burndown/",
        ProjectBurndownAnalyticsEndpoint.as_view(),
        name="project-burndown-analytics",
    ),
    path(
        "workspaces/<str:slug>/projects/<uuid:project_id>/analytics/velocity/",
        ProjectVelocityAnalyticsEndpoint.as_view(),
        name="project-velocity-analytics",
    ),
    path(
        "workspaces/<str:slug>/projects/<uuid:project_id>/analytics/flow/",
        ProjectFlowAnalyticsEndpoint.as_view(),
        name="project-flow-analytics",
    ),
    path(
        "workspaces/<str:slug>/projects/<uuid:project_id>/analytics/workload/",
        ProjectWorkloadAnalyticsEndpoint.as_view(),
        name="project-workload-analytics",
    ),
]
