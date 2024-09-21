from rest_framework import serializers
from taskite.models import User, WorkspaceInvite, Workspace


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ["id", "name", "created_at"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "created_at",
            "is_verified",
        ]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField()


class WorkspaceInviteSerializer(serializers.ModelSerializer):
    invited_by = UserSerializer()
    workspace = WorkspaceSerializer()

    class Meta:
        model = WorkspaceInvite
        fields = [
            "id",
            "workspace",
            "email",
            "invited_by",
            "confirmation_link",
            "rejection_link",
            "created_at",
        ]
