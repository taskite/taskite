from rest_framework import serializers

from calyvim.models.workspace import WorkspaceInvite, WorkspaceMembership
from calyvim.models.user import User


class InvitedBySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "display_name", "last_name"]


class WorkspaceInviteSerializer(serializers.ModelSerializer):
    invited_by = InvitedBySerializer()

    class Meta:
        model = WorkspaceInvite
        fields = ["id", "email", "confirmed_at", "invited_by", "created_at"]


class WorkspaceInviteCreateSerializer(serializers.Serializer):
    emails = serializers.ListField(
        child=serializers.CharField(), allow_empty=False, min_length=1
    )
    role = serializers.ChoiceField(choices=WorkspaceMembership.Role.choices)
