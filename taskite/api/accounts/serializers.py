from rest_framework import serializers
from taskite.mixins import FileNameAndSourceSerializerMixin
from taskite.models import User, WorkspaceInvite, Workspace
from rest_framework.exceptions import ValidationError


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ["id", "name", "created_at"]


class UserSerializer(FileNameAndSourceSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "avatar",
            "created_at",
            "is_verified",
        ]


class UserUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False, allow_null=True)
    avatar = serializers.CharField(required=False, allow_null=True)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField()
    last_name = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField()
    invitation_id = serializers.CharField(required=False)

    def validate(self, data):
        if not data.get("invitation_id") and not data.get("email"):
            raise ValidationError("Either 'invitation_id' or 'email' must be provided.")
        return data


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
