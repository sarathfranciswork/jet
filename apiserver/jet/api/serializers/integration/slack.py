# Module imports
from jet.api.serializers import BaseSerializer
from jet.db.models import SlackProjectSync


class SlackProjectSyncSerializer(BaseSerializer):
    class Meta:
        model = SlackProjectSync
        fields = "__all__"
        read_only_fields = [
            "project",
            "workspace",
            "workspace_integration",
        ]
