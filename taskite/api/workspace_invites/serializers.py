from rest_framework import serializers

from taskite.models.workspace import WorkspaceInvite
from taskite.models.user import User


class InvitedBySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name"]


class WorkspaceInviteSerializer(serializers.ModelSerializer):
    invited_by = InvitedBySerializer()

    class Meta:
        model = WorkspaceInvite
        fields = ["id", "email", "accepted", "invited_by", "created_at"]
