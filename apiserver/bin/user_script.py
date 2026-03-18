import os, sys
import uuid

sys.path.append("/code")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jet.settings.production")
import django

django.setup()

from jet.db.models import User


def populate():
    default_email = os.environ.get("DEFAULT_EMAIL", "admin@jetpm.app")
    default_password = os.environ.get("DEFAULT_PASSWORD", "password123")

    if not User.objects.filter(email=default_email).exists():
        user = User.objects.create(email=default_email, username=uuid.uuid4().hex)
        user.set_password(default_password)
        user.save()
        print(f"User created with an email: {default_email}")
    else:
        print(f"User already exists with the default email: {default_email}")


if __name__ == "__main__":
    populate()
