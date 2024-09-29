from rest_framework import serializers

from taskite.mixins import NameAndSourceSerializerMixin
from taskite.models import Workspace, WorkspaceMembership, User


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "avatar",
            "first_name",
            "last_name",
        ]


class WorkspaceSerializer(NameAndSourceSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ["id", "name", "slug", "logo", "description", "created_at"]


class WorkspaceCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )


class WorkspaceMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceMembership
        fields = ["id", "workspace_id", "role", "created_at"]


class WorkspaceUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    logo = serializers.CharField(required=False, allow_null=True)
