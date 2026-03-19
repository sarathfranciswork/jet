# Python imports
import uuid

# Django imports
from django.db import models

# Module imports
from jet.db.models import ProjectBaseModel
from jet.db.models.base import BaseModel


class GithubRepository(ProjectBaseModel):
    name = models.CharField(max_length=500)
    url = models.URLField(null=True)
    config = models.JSONField(default=dict)
    repository_id = models.BigIntegerField()
    owner = models.CharField(max_length=500)

    def __str__(self):
        """Return the repo name"""
        return f"{self.name}"

    class Meta:
        verbose_name = "Repository"
        verbose_name_plural = "Repositories"
        db_table = "github_repositories"
        ordering = ("-created_at",)


class GithubRepositorySync(ProjectBaseModel):
    repository = models.OneToOneField(
        "db.GithubRepository", on_delete=models.CASCADE, related_name="syncs"
    )
    credentials = models.JSONField(default=dict)
    # Bot user
    actor = models.ForeignKey(
        "db.User", related_name="user_syncs", on_delete=models.CASCADE
    )
    workspace_integration = models.ForeignKey(
        "db.WorkspaceIntegration", related_name="github_syncs", on_delete=models.CASCADE
    )
    label = models.ForeignKey(
        "db.Label", on_delete=models.SET_NULL, null=True, related_name="repo_syncs"
    )

    def __str__(self):
        """Return the repo sync"""
        return f"{self.repository.name} <{self.project.name}>"

    class Meta:
        unique_together = ["project", "repository"]
        verbose_name = "Github Repository Sync"
        verbose_name_plural = "Github Repository Syncs"
        db_table = "github_repository_syncs"
        ordering = ("-created_at",)


class GithubIssueSync(ProjectBaseModel):
    repo_issue_id = models.BigIntegerField()
    github_issue_id = models.BigIntegerField()
    issue_url = models.URLField(blank=False)
    issue = models.ForeignKey(
        "db.Issue", related_name="github_syncs", on_delete=models.CASCADE
    )
    repository_sync = models.ForeignKey(
        "db.GithubRepositorySync", related_name="issue_syncs", on_delete=models.CASCADE
    )
    github_issue_number = models.IntegerField(null=True, blank=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """Return the github issue sync"""
        return f"{self.repository_sync.repository.name}-{self.project.name}-{self.issue.name}"

    class Meta:
        unique_together = ["repository_sync", "issue"]
        verbose_name = "Github Issue Sync"
        verbose_name_plural = "Github Issue Syncs"
        db_table = "github_issue_syncs"
        ordering = ("-created_at",)


class GithubCommentSync(ProjectBaseModel):
    repo_comment_id = models.BigIntegerField()
    comment = models.ForeignKey(
        "db.IssueComment", related_name="comment_syncs", on_delete=models.CASCADE
    )
    issue_sync = models.ForeignKey(
        "db.GithubIssueSync", related_name="comment_syncs", on_delete=models.CASCADE
    )
    last_synced_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """Return the github issue sync"""
        return f"{self.comment.id}"

    class Meta:
        unique_together = ["issue_sync", "comment"]
        verbose_name = "Github Comment Sync"
        verbose_name_plural = "Github Comment Syncs"
        db_table = "github_comment_syncs"
        ordering = ("-created_at",)


SYNC_DIRECTION_CHOICES = (
    ("bidirectional", "Bidirectional"),
    ("github_to_jet", "GitHub to Jet"),
)

SYNC_ENTITY_CHOICES = (
    ("issue", "Issue"),
    ("comment", "Comment"),
    ("label", "Label"),
    ("pull_request", "Pull Request"),
    ("state", "State"),
    ("assignee", "Assignee"),
)

SYNC_DIRECTION_LOG_CHOICES = (
    ("github_to_jet", "GitHub to Jet"),
    ("jet_to_github", "Jet to GitHub"),
)

SYNC_STATUS_CHOICES = (
    ("success", "Success"),
    ("failed", "Failed"),
    ("skipped", "Skipped"),
)

PR_STATE_CHOICES = (
    ("draft", "Draft"),
    ("open", "Open"),
    ("closed", "Closed"),
    ("merged", "Merged"),
)


class GithubSyncConfig(ProjectBaseModel):
    repository_sync = models.OneToOneField(
        "db.GithubRepositorySync",
        on_delete=models.CASCADE,
        related_name="sync_config",
    )
    sync_direction = models.CharField(
        max_length=20,
        choices=SYNC_DIRECTION_CHOICES,
        default="bidirectional",
    )
    github_trigger_label = models.CharField(
        max_length=255,
        default="Jet",
        help_text="Label on GitHub issues that triggers Jet issue creation",
    )
    jet_trigger_label = models.ForeignKey(
        "db.Label",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="github_sync_triggers",
        help_text="Jet label that triggers GitHub issue creation",
    )
    state_mapping = models.JSONField(
        default=dict,
        help_text='Maps GitHub issue states to Jet state UUIDs, e.g. {"open": "<uuid>", "closed": "<uuid>"}',
    )
    pr_state_mapping = models.JSONField(
        default=dict,
        help_text='Maps PR lifecycle states to Jet state UUIDs, e.g. {"draft": "<uuid>", "open": "<uuid>", "merged": "<uuid>"}',
    )
    sync_comments = models.BooleanField(default=True)
    sync_labels = models.BooleanField(default=True)
    sync_assignees = models.BooleanField(default=True)
    webhook_secret = models.CharField(max_length=255, blank=True, default="")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"SyncConfig: {self.repository_sync}"

    class Meta:
        verbose_name = "Github Sync Config"
        verbose_name_plural = "Github Sync Configs"
        db_table = "github_sync_configs"
        ordering = ("-created_at",)


class GithubPullRequest(ProjectBaseModel):
    pr_number = models.IntegerField()
    github_pr_id = models.BigIntegerField()
    title = models.CharField(max_length=1000)
    url = models.URLField()
    state = models.CharField(max_length=20, choices=PR_STATE_CHOICES, default="open")
    is_draft = models.BooleanField(default=False)
    issue = models.ForeignKey(
        "db.Issue",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="github_pull_requests",
    )
    repository_sync = models.ForeignKey(
        "db.GithubRepositorySync",
        on_delete=models.CASCADE,
        related_name="pull_requests",
    )
    triggers_automation = models.BooleanField(
        default=False,
        help_text="True if PR uses bracket notation [WEB-123] for state automation",
    )
    author_login = models.CharField(max_length=255, blank=True, default="")
    author_avatar_url = models.URLField(blank=True, default="")
    merged_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PR #{self.pr_number}: {self.title}"

    class Meta:
        unique_together = ["repository_sync", "pr_number"]
        verbose_name = "Github Pull Request"
        verbose_name_plural = "Github Pull Requests"
        db_table = "github_pull_requests"
        ordering = ("-created_at",)


class GithubUserMapping(BaseModel):
    workspace = models.ForeignKey(
        "db.Workspace",
        on_delete=models.CASCADE,
        related_name="github_user_mappings",
    )
    user = models.ForeignKey(
        "db.User",
        on_delete=models.CASCADE,
        related_name="github_user_mappings",
    )
    github_user_id = models.BigIntegerField()
    github_username = models.CharField(max_length=255)
    github_access_token = models.CharField(
        max_length=500,
        blank=True,
        default="",
        help_text="GitHub access token for comment attribution",
    )

    def __str__(self):
        return f"{self.user.email} <-> {self.github_username}"

    class Meta:
        unique_together = ["workspace", "user"]
        verbose_name = "Github User Mapping"
        verbose_name_plural = "Github User Mappings"
        db_table = "github_user_mappings"
        ordering = ("-created_at",)


class GithubSyncLog(ProjectBaseModel):
    repository_sync = models.ForeignKey(
        "db.GithubRepositorySync",
        on_delete=models.CASCADE,
        related_name="sync_logs",
    )
    entity_type = models.CharField(max_length=20, choices=SYNC_ENTITY_CHOICES)
    entity_id = models.CharField(max_length=255, help_text="ID of the synced entity")
    direction = models.CharField(max_length=20, choices=SYNC_DIRECTION_LOG_CHOICES)
    status = models.CharField(max_length=20, choices=SYNC_STATUS_CHOICES)
    error_message = models.TextField(blank=True, default="")
    payload = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.entity_type} {self.direction} {self.status}"

    class Meta:
        verbose_name = "Github Sync Log"
        verbose_name_plural = "Github Sync Logs"
        db_table = "github_sync_logs"
        ordering = ("-created_at",)
