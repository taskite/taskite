from rest_framework import serializers

from calyvim.models import BoardTeamPermission, Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name", "avatar", "created_at"]


class BoardTeamPermissionSerializer(serializers.ModelSerializer):
    team = TeamSerializer()

    class Meta:
        model = BoardTeamPermission
        fields = ["id", "team", "role", "created_at"]


class BoardTeamCreateSerializer(serializers.Serializer):
    team_id = serializers.UUIDField()
    role = serializers.CharField()


class BoardTeamPermissionUpdateSerializer(serializers.Serializer):
    role = serializers.CharField()