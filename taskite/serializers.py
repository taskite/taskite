from rest_framework import serializers

from taskite.models import Workspace, User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name"
        ]


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "created_at",
        ]
