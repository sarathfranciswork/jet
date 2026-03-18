from django.db import migrations


def update_content_types(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    # Update any content types that might reference 'plane' app labels
    for ct in ContentType.objects.filter(app_label__contains="plane"):
        ct.app_label = ct.app_label.replace("plane", "jet")
        ct.save()


def reverse_content_types(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    for ct in ContentType.objects.filter(app_label__contains="jet"):
        ct.app_label = ct.app_label.replace("jet", "plane")
        ct.save()


class Migration(migrations.Migration):
    dependencies = [
        ("db", "0046_alter_analyticview_created_by_and_more"),
    ]
    operations = [
        migrations.RunPython(update_content_types, reverse_content_types),
    ]
