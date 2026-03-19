# Django imports
from django.db.models import Count, Sum, F, Q
from django.db.models.functions import (
    TruncDate,
    ExtractIsoWeekDay,
)
from django.utils import timezone

# Third party imports
from rest_framework import status
from rest_framework.response import Response

# Module imports
from plane.api.views import BaseAPIView
from plane.api.permissions import ProjectEntityPermission
from plane.db.models import Issue, Cycle, CycleIssue, IssueActivity, State

from datetime import timedelta
import csv
import io


class ProjectBurndownAnalyticsEndpoint(BaseAPIView):
    permission_classes = [ProjectEntityPermission]

    def get(self, request, slug, project_id):
        cycle_id = request.GET.get("cycle_id")
        metric = request.GET.get("metric", "count")

        if not cycle_id:
            return Response(
                {"error": "cycle_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if metric not in ("count", "points"):
            return Response(
                {"error": "metric must be 'count' or 'points'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            cycle = Cycle.objects.get(
                pk=cycle_id,
                project_id=project_id,
                workspace__slug=slug,
            )
        except Cycle.DoesNotExist:
            return Response(
                {"error": "Cycle not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not cycle.start_date or not cycle.end_date:
            return Response(
                {"error": "Cycle must have start and end dates"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get all issues in this cycle
        cycle_issues = Issue.issue_objects.filter(
            workspace__slug=slug,
            project_id=project_id,
            issue_cycle__cycle_id=cycle_id,
        )

        # Total scope
        if metric == "points":
            total_scope = cycle_issues.aggregate(
                total=Sum("estimate_point")
            )["total"] or 0
        else:
            total_scope = cycle_issues.count()

        # Build daily burndown
        start = cycle.start_date
        end = cycle.end_date
        total_days = (end - start).days
        if total_days <= 0:
            total_days = 1

        # Get completion data: issues completed per day
        completed_per_day = (
            cycle_issues.filter(completed_at__isnull=False)
            .annotate(completed_date=TruncDate("completed_at"))
            .values("completed_date")
        )

        if metric == "points":
            completed_per_day = completed_per_day.annotate(
                value=Sum("estimate_point")
            )
        else:
            completed_per_day = completed_per_day.annotate(
                value=Count("id")
            )

        completed_per_day = completed_per_day.order_by("completed_date")

        # Build a map of date -> completed value
        completion_map = {}
        for entry in completed_per_day:
            if entry["completed_date"]:
                completion_map[entry["completed_date"]] = entry["value"] or 0

        # Detect scope changes: issues added to cycle after start
        scope_changes = (
            CycleIssue.objects.filter(
                cycle_id=cycle_id,
                workspace__slug=slug,
                project_id=project_id,
                created_at__date__gt=start,
            )
            .annotate(added_date=TruncDate("created_at"))
            .values("added_date")
            .annotate(count=Count("id"))
            .order_by("added_date")
        )

        scope_change_map = {}
        for entry in scope_changes:
            if entry["added_date"]:
                scope_change_map[entry["added_date"]] = entry["count"]

        # Build daily data
        ideal_data = []
        actual_data = []
        scope_change_markers = []

        remaining = total_scope
        current_scope = total_scope

        current_date = start
        day_index = 0

        while current_date <= end:
            # Ideal burndown (linear)
            ideal_remaining = total_scope - (
                total_scope * day_index / total_days
            )
            ideal_data.append(
                {"date": current_date.isoformat(), "value": round(ideal_remaining, 1)}
            )

            # Track scope changes
            added = scope_change_map.get(current_date, 0)
            if added > 0:
                if metric == "points":
                    # Get actual points added
                    added_points = (
                        Issue.issue_objects.filter(
                            issue_cycle__cycle_id=cycle_id,
                            issue_cycle__created_at__date=current_date,
                            workspace__slug=slug,
                            project_id=project_id,
                        ).aggregate(total=Sum("estimate_point"))["total"]
                        or 0
                    )
                    remaining += added_points
                    current_scope += added_points
                else:
                    remaining += added
                    current_scope += added
                scope_change_markers.append(
                    {"date": current_date.isoformat(), "added": added}
                )

            # Subtract completed
            completed = completion_map.get(current_date, 0)
            remaining -= completed

            actual_data.append(
                {"date": current_date.isoformat(), "value": max(remaining, 0)}
            )

            current_date += timedelta(days=1)
            day_index += 1

        return Response(
            {
                "ideal": ideal_data,
                "actual": actual_data,
                "scope_changes": scope_change_markers,
                "total_scope": current_scope,
                "metric": metric,
                "cycle": {
                    "id": str(cycle.id),
                    "name": cycle.name,
                    "start_date": cycle.start_date.isoformat(),
                    "end_date": cycle.end_date.isoformat(),
                },
            },
            status=status.HTTP_200_OK,
        )


class ProjectVelocityAnalyticsEndpoint(BaseAPIView):
    permission_classes = [ProjectEntityPermission]

    def get(self, request, slug, project_id):
        last_n_cycles = int(request.GET.get("last_n_cycles", 6))
        last_n_cycles = min(last_n_cycles, 20)  # Cap at 20

        # Get completed cycles (those with end_date in the past)
        cycles = (
            Cycle.objects.filter(
                project_id=project_id,
                workspace__slug=slug,
                start_date__isnull=False,
                end_date__isnull=False,
            )
            .order_by("-end_date")[:last_n_cycles]
        )

        velocity_data = []
        for cycle in reversed(list(cycles)):
            cycle_issues = Issue.issue_objects.filter(
                issue_cycle__cycle_id=cycle.id,
                workspace__slug=slug,
                project_id=project_id,
            )

            completed_issues = cycle_issues.filter(
                completed_at__isnull=False,
            )

            total_count = cycle_issues.count()
            completed_count = completed_issues.count()
            completed_points = (
                completed_issues.aggregate(total=Sum("estimate_point"))["total"] or 0
            )
            committed_points = (
                cycle_issues.aggregate(total=Sum("estimate_point"))["total"] or 0
            )

            velocity_data.append(
                {
                    "cycle_id": str(cycle.id),
                    "cycle_name": cycle.name,
                    "start_date": cycle.start_date.isoformat() if cycle.start_date else None,
                    "end_date": cycle.end_date.isoformat() if cycle.end_date else None,
                    "completed_issues": completed_count,
                    "total_issues": total_count,
                    "completed_points": completed_points,
                    "committed_points": committed_points,
                }
            )

        # Calculate rolling average (last 4 cycles)
        rolling_window = 4
        rolling_averages = []
        for i in range(len(velocity_data)):
            start_idx = max(0, i - rolling_window + 1)
            window = velocity_data[start_idx : i + 1]
            avg_points = sum(v["completed_points"] for v in window) / len(window)
            avg_count = sum(v["completed_issues"] for v in window) / len(window)
            rolling_averages.append(
                {
                    "cycle_name": velocity_data[i]["cycle_name"],
                    "avg_points": round(avg_points, 1),
                    "avg_count": round(avg_count, 1),
                }
            )

        return Response(
            {
                "velocity": velocity_data,
                "rolling_average": rolling_averages,
            },
            status=status.HTTP_200_OK,
        )


class ProjectFlowAnalyticsEndpoint(BaseAPIView):
    permission_classes = [ProjectEntityPermission]

    def get(self, request, slug, project_id):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        if not start_date or not end_date:
            return Response(
                {"error": "start_date and end_date are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            from datetime import date as date_type

            start = date_type.fromisoformat(start_date)
            end = date_type.fromisoformat(end_date)
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (end - start).days > 365:
            return Response(
                {"error": "Date range cannot exceed 365 days"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # State groups in order
        state_groups = ["backlog", "unstarted", "started", "completed", "cancelled"]

        # Get all state change activities in the date range for this project
        state_changes = (
            IssueActivity.objects.filter(
                issue__project_id=project_id,
                workspace__slug=slug,
                field="state",
                created_at__date__gte=start,
                created_at__date__lte=end,
                issue__archived_at__isnull=True,
                issue__is_draft=False,
            )
            .annotate(activity_date=TruncDate("created_at"))
            .values("activity_date", "issue_id", "new_identifier")
            .order_by("activity_date", "created_at")
        )

        # Get initial state distribution (as of start_date)
        project_issues = Issue.issue_objects.filter(
            project_id=project_id,
            workspace__slug=slug,
            created_at__date__lte=start,
        )

        initial_counts = {}
        for group in state_groups:
            initial_counts[group] = project_issues.filter(
                state__group=group
            ).count()

        # Build state map for lookups
        states = State.objects.filter(
            project_id=project_id,
            workspace__slug=slug,
        ).values("id", "group")
        state_group_map = {str(s["id"]): s["group"] for s in states}

        # Build daily flow data
        flow_data = []
        current_counts = dict(initial_counts)
        current_date = start

        # Pre-process state changes by date
        changes_by_date = {}
        for change in state_changes:
            d = change["activity_date"]
            if d not in changes_by_date:
                changes_by_date[d] = []
            changes_by_date[d].append(change)

        # Also count new issues created per day
        new_issues_by_date = (
            Issue.issue_objects.filter(
                project_id=project_id,
                workspace__slug=slug,
                created_at__date__gt=start,
                created_at__date__lte=end,
            )
            .annotate(created_date=TruncDate("created_at"))
            .values("created_date", "state__group")
            .annotate(count=Count("id"))
            .order_by("created_date")
        )

        new_issues_map = {}
        for entry in new_issues_by_date:
            d = entry["created_date"]
            if d not in new_issues_map:
                new_issues_map[d] = {}
            new_issues_map[d][entry["state__group"]] = entry["count"]

        while current_date <= end:
            # Add new issues created on this day
            if current_date in new_issues_map:
                for group, count in new_issues_map[current_date].items():
                    if group in current_counts:
                        current_counts[group] += count

            # Process state changes for this day
            if current_date in changes_by_date:
                for change in changes_by_date[current_date]:
                    new_state_id = str(change["new_identifier"]) if change["new_identifier"] else None
                    if new_state_id and new_state_id in state_group_map:
                        new_group = state_group_map[new_state_id]
                        # We track net changes - the old state group decreases,
                        # new state group increases. Since we don't have old_identifier
                        # reliably mapped, we use the activity's old_identifier field
                        # This is a simplified approach using cumulative counts
                        pass

            flow_data.append(
                {
                    "date": current_date.isoformat(),
                    **{group: max(current_counts.get(group, 0), 0) for group in state_groups},
                }
            )

            current_date += timedelta(days=1)

        # For a more accurate approach, recalculate from scratch per day
        # by querying the actual state distribution
        # This is more expensive but accurate for the MVP
        flow_data_accurate = []
        current_date = start
        while current_date <= end:
            day_counts = {}
            for group in state_groups:
                count = Issue.issue_objects.filter(
                    project_id=project_id,
                    workspace__slug=slug,
                    created_at__date__lte=current_date,
                ).filter(
                    # Issues that are currently in this state group
                    # OR were in this group as of this date
                    Q(state__group=group, completed_at__isnull=True)
                    | Q(state__group=group, completed_at__date__gte=current_date)
                    | Q(
                        state__group=group,
                        completed_at__date__lte=current_date,
                    )
                ).count()
                day_counts[group] = count

            flow_data_accurate.append(
                {
                    "date": current_date.isoformat(),
                    **day_counts,
                }
            )
            current_date += timedelta(days=1)

        # Use simplified approach based on current snapshot projected
        # For better perf, use the initial_counts + changes approach
        # Recalculate properly: get current state distribution per day
        # by looking at the current state of each issue
        current_date = start
        flow_result = []

        # Get all project issues created before or during range
        all_issues = Issue.issue_objects.filter(
            project_id=project_id,
            workspace__slug=slug,
        ).values("id", "state__group", "created_at", "completed_at")

        issues_list = list(all_issues)

        while current_date <= end:
            day_counts = {group: 0 for group in state_groups}
            for issue in issues_list:
                # Only count if issue existed by this date
                if issue["created_at"].date() <= current_date:
                    group = issue["state__group"]
                    if group in day_counts:
                        day_counts[group] += 1

            flow_result.append(
                {
                    "date": current_date.isoformat(),
                    **day_counts,
                }
            )
            current_date += timedelta(days=1)

        return Response(
            {
                "flow": flow_result,
                "state_groups": state_groups,
            },
            status=status.HTTP_200_OK,
        )


class ProjectWorkloadAnalyticsEndpoint(BaseAPIView):
    permission_classes = [ProjectEntityPermission]

    def get(self, request, slug, project_id):
        cycle_id = request.GET.get("cycle_id")

        base_filter = Q(
            workspace__slug=slug,
            project_id=project_id,
            completed_at__isnull=False,
        )

        if cycle_id:
            base_filter &= Q(issue_cycle__cycle_id=cycle_id)

        # Get completed issues with assignee and day of week
        workload_data = (
            Issue.issue_objects.filter(base_filter)
            .filter(assignees__isnull=False)
            .annotate(
                weekday=ExtractIsoWeekDay("completed_at"),
            )
            .values(
                "assignees__id",
                "assignees__display_name",
                "assignees__avatar",
                "weekday",
            )
            .annotate(count=Count("id"))
            .order_by("assignees__display_name", "weekday")
        )

        # Organize into a structured response
        # weekday: 1=Monday, 7=Sunday (ISO)
        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        assignee_map = {}
        for entry in workload_data:
            assignee_id = str(entry["assignees__id"])
            if assignee_id not in assignee_map:
                assignee_map[assignee_id] = {
                    "assignee_id": assignee_id,
                    "display_name": entry["assignees__display_name"],
                    "avatar": entry["assignees__avatar"],
                    "days": {day: 0 for day in day_names},
                    "total": 0,
                }
            # ExtractIsoWeekDay: 1=Monday, 7=Sunday
            weekday_idx = entry["weekday"] - 1
            if 0 <= weekday_idx < 7:
                day = day_names[weekday_idx]
                assignee_map[assignee_id]["days"][day] = entry["count"]
                assignee_map[assignee_id]["total"] += entry["count"]

        workload = sorted(
            assignee_map.values(), key=lambda x: x["total"], reverse=True
        )

        return Response(
            {
                "workload": workload,
                "days": day_names,
            },
            status=status.HTTP_200_OK,
        )
