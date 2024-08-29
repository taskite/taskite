from rest_framework import serializers

from taskite.models import Workspace, WorkspaceMembership


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ["id", "name", "description", "created_at"]


class WorkspaceMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceMembership
        fields = ["id", "workspace_id", "role", "created_at"]
