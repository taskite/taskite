from rest_framework import serializers

from taskite.models import Workspace, WorkspaceMembership, User


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
        ]


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ["id", "name", "description", "created_at"]


class WorkspaceMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceMembership
        fields = ["id", "workspace_id", "role", "created_at"]
