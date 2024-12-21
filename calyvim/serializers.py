from rest_framework import serializers

from calyvim.mixins import NameAndSourceSerializerMixin
from calyvim.models import Workspace, User, Team, Board, Sprint


class ProfileSerializer(NameAndSourceSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "display_name",
            "avatar",
        ]


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
        fields = [
            "id",
            "name",
            "slug",
            "cover",
            "description",
            "is_estimate_enabled",
            "created_at",
        ]


class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ["id", "name", "start_date", "end_date", "is_active", "created_at"]
