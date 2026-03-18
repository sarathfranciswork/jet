# Module imports
from jet.api.serializers import BaseSerializer
from jet.db.models import Integration, WorkspaceIntegration


class IntegrationSerializer(BaseSerializer):
    class Meta:
        model = Integration
        fields = "__all__"
        read_only_fields = [
            "verified",
        ]


class WorkspaceIntegrationSerializer(BaseSerializer):
    integration_detail = IntegrationSerializer(read_only=True, source="integration")

    class Meta:
        model = WorkspaceIntegration
        fields = "__all__"
