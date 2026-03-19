# Data migration to seed GitHub and Slack integration records

from django.db import migrations


def seed_integrations(apps, schema_editor):
    Integration = apps.get_model("db", "Integration")

    # Create GitHub integration if not exists
    if not Integration.objects.filter(provider="github").exists():
        Integration.objects.create(
            title="GitHub",
            provider="github",
            network=2,  # Public
            description="Connect with GitHub to sync project issues, pull requests, and automate workflows.",
            verified=True,
            redirect_url="",
            webhook_url="",
            metadata={},
        )

    # Create Slack integration if not exists
    if not Integration.objects.filter(provider="slack").exists():
        Integration.objects.create(
            title="Slack",
            provider="slack",
            network=2,  # Public
            description="Connect with Slack to sync project issues and notifications with channels.",
            verified=True,
            redirect_url="",
            webhook_url="",
            metadata={},
        )


def reverse_seed(apps, schema_editor):
    Integration = apps.get_model("db", "Integration")
    Integration.objects.filter(provider__in=["github", "slack"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("db", "0048_github_full_integration"),
    ]

    operations = [
        migrations.RunPython(seed_integrations, reverse_seed),
    ]
