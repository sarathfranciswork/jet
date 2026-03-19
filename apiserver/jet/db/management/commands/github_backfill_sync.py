"""Management command to backfill GithubSyncConfig for existing GithubRepositorySync records."""
from django.core.management.base import BaseCommand

from jet.db.models import GithubRepositorySync, GithubSyncConfig


class Command(BaseCommand):
    help = "Create GithubSyncConfig for existing GithubRepositorySync records that don't have one"

    def add_arguments(self, parser):
        parser.add_argument(
            "--activate",
            action="store_true",
            default=False,
            help="Set is_active=True on newly created configs (default: False)",
        )

    def handle(self, *args, **options):
        activate = options["activate"]

        repo_syncs = GithubRepositorySync.objects.select_related(
            "repository"
        ).all()

        created_count = 0
        skipped_count = 0

        for repo_sync in repo_syncs:
            if GithubSyncConfig.objects.filter(repository_sync=repo_sync).exists():
                skipped_count += 1
                self.stdout.write(
                    f"  Skipped: {repo_sync.repository.name} (config exists)"
                )
                continue

            GithubSyncConfig.objects.create(
                repository_sync=repo_sync,
                sync_direction="bidirectional",
                github_trigger_label="Jet",
                is_active=activate,
                project_id=repo_sync.project_id,
                workspace_id=repo_sync.workspace_id,
            )
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f"  Created config for: {repo_sync.repository.name}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone. Created: {created_count}, Skipped: {skipped_count}"
            )
        )
