from rest_framework import serializers

from taskite.mixins import NameAndSourceSerializerMixin
from taskite.models import Workspace, User, Team, Board


class ProfileSerializer(NameAndSourceSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "display_name", "avatar"]


class WorkspaceSerializer(NameAndSourceSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = [
            "id",
            "name",
            "slug",
            "logo",
            "description",
            "created_at",
        ]


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name", "created_at"]


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["id", "name", "slug", "cover", "description", "created_at"]
