from .base import BaseSerializer
from jet.db.models import APIToken


class APITokenSerializer(BaseSerializer):
    class Meta:
        model = APIToken
        fields = [
            "label",
            "user",
            "user_type",
            "workspace",
            "created_at",
        ]
