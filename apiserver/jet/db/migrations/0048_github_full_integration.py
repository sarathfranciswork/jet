# Generated migration for GitHub full integration

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("db", "0047_update_content_types"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Extend GithubIssueSync with new fields
        migrations.AddField(
            model_name="githubissuesync",
            name="github_issue_number",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="githubissuesync",
            name="last_synced_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        # Extend GithubCommentSync with new field
        migrations.AddField(
            model_name="githubcommentsync",
            name="last_synced_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        # GithubSyncConfig
        migrations.CreateModel(
            name="GithubSyncConfig",
            fields=[
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Last Modified At"),
                ),
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "sync_direction",
                    models.CharField(
                        choices=[
                            ("bidirectional", "Bidirectional"),
                            ("github_to_jet", "GitHub to Jet"),
                        ],
                        default="bidirectional",
                        max_length=20,
                    ),
                ),
                (
                    "github_trigger_label",
                    models.CharField(
                        default="Jet",
                        help_text="Label on GitHub issues that triggers Jet issue creation",
                        max_length=255,
                    ),
                ),
                (
                    "state_mapping",
                    models.JSONField(
                        default=dict,
                        help_text='Maps GitHub issue states to Jet state UUIDs',
                    ),
                ),
                (
                    "pr_state_mapping",
                    models.JSONField(
                        default=dict,
                        help_text='Maps PR lifecycle states to Jet state UUIDs',
                    ),
                ),
                ("sync_comments", models.BooleanField(default=True)),
                ("sync_labels", models.BooleanField(default=True)),
                ("sync_assignees", models.BooleanField(default=True)),
                (
                    "webhook_secret",
                    models.CharField(blank=True, default="", max_length=255),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_updated_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Last Modified By",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="project_%(class)s",
                        to="db.project",
                    ),
                ),
                (
                    "workspace",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="workspace_%(class)s",
                        to="db.workspace",
                    ),
                ),
                (
                    "repository_sync",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sync_config",
                        to="db.githubrepositorysync",
                    ),
                ),
                (
                    "jet_trigger_label",
                    models.ForeignKey(
                        blank=True,
                        help_text="Jet label that triggers GitHub issue creation",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="github_sync_triggers",
                        to="db.label",
                    ),
                ),
            ],
            options={
                "verbose_name": "Github Sync Config",
                "verbose_name_plural": "Github Sync Configs",
                "db_table": "github_sync_configs",
                "ordering": ("-created_at",),
            },
        ),
        # GithubPullRequest
        migrations.CreateModel(
            name="GithubPullRequest",
            fields=[
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Last Modified At"),
                ),
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("pr_number", models.IntegerField()),
                ("github_pr_id", models.BigIntegerField()),
                ("title", models.CharField(max_length=1000)),
                ("url", models.URLField()),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("open", "Open"),
                            ("closed", "Closed"),
                            ("merged", "Merged"),
                        ],
                        default="open",
                        max_length=20,
                    ),
                ),
                ("is_draft", models.BooleanField(default=False)),
                (
                    "triggers_automation",
                    models.BooleanField(
                        default=False,
                        help_text="True if PR uses bracket notation [WEB-123] for state automation",
                    ),
                ),
                (
                    "author_login",
                    models.CharField(blank=True, default="", max_length=255),
                ),
                (
                    "author_avatar_url",
                    models.URLField(blank=True, default=""),
                ),
                ("merged_at", models.DateTimeField(blank=True, null=True)),
                ("closed_at", models.DateTimeField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_updated_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Last Modified By",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="project_%(class)s",
                        to="db.project",
                    ),
                ),
                (
                    "workspace",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="workspace_%(class)s",
                        to="db.workspace",
                    ),
                ),
                (
                    "issue",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="github_pull_requests",
                        to="db.issue",
                    ),
                ),
                (
                    "repository_sync",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pull_requests",
                        to="db.githubrepositorysync",
                    ),
                ),
            ],
            options={
                "verbose_name": "Github Pull Request",
                "verbose_name_plural": "Github Pull Requests",
                "db_table": "github_pull_requests",
                "ordering": ("-created_at",),
                "unique_together": {("repository_sync", "pr_number")},
            },
        ),
        # GithubUserMapping
        migrations.CreateModel(
            name="GithubUserMapping",
            fields=[
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Last Modified At"),
                ),
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("github_user_id", models.BigIntegerField()),
                ("github_username", models.CharField(max_length=255)),
                (
                    "github_access_token",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="GitHub access token for comment attribution",
                        max_length=500,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_updated_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Last Modified By",
                    ),
                ),
                (
                    "workspace",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="github_user_mappings",
                        to="db.workspace",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="github_user_mappings",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Github User Mapping",
                "verbose_name_plural": "Github User Mappings",
                "db_table": "github_user_mappings",
                "ordering": ("-created_at",),
                "unique_together": {("workspace", "user")},
            },
        ),
        # GithubSyncLog
        migrations.CreateModel(
            name="GithubSyncLog",
            fields=[
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Last Modified At"),
                ),
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "entity_type",
                    models.CharField(
                        choices=[
                            ("issue", "Issue"),
                            ("comment", "Comment"),
                            ("label", "Label"),
                            ("pull_request", "Pull Request"),
                            ("state", "State"),
                            ("assignee", "Assignee"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "entity_id",
                    models.CharField(
                        help_text="ID of the synced entity",
                        max_length=255,
                    ),
                ),
                (
                    "direction",
                    models.CharField(
                        choices=[
                            ("github_to_jet", "GitHub to Jet"),
                            ("jet_to_github", "Jet to GitHub"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("success", "Success"),
                            ("failed", "Failed"),
                            ("skipped", "Skipped"),
                        ],
                        max_length=20,
                    ),
                ),
                ("error_message", models.TextField(blank=True, default="")),
                ("payload", models.JSONField(blank=True, default=dict)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_updated_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Last Modified By",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="project_%(class)s",
                        to="db.project",
                    ),
                ),
                (
                    "workspace",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="workspace_%(class)s",
                        to="db.workspace",
                    ),
                ),
                (
                    "repository_sync",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sync_logs",
                        to="db.githubrepositorysync",
                    ),
                ),
            ],
            options={
                "verbose_name": "Github Sync Log",
                "verbose_name_plural": "Github Sync Logs",
                "db_table": "github_sync_logs",
                "ordering": ("-created_at",),
            },
        ),
    ]
