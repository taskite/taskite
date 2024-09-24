from rest_framework import serializers

from taskite.models.workspace import WorkspaceMembership
from taskite.models.user import User
from taskite.models.team import Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name", "created_at"]


class UserSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many=True)

    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name", "teams"]


class WorkspaceMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = WorkspaceMembership
        fields = ["id", "role", "user", "created_at"]


class WorkspaceMembershipUpdateSerializer(serializers.Serializer):
    role = serializers.CharField()