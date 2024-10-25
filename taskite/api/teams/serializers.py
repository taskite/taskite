from rest_framework import serializers

from taskite.models.team import Team
from taskite.models.user import User


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
            "display_name",
        ]


class TeamSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "avatar",
            "members",
            "created_at",
        ]


class TeamCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField(
        required=False, allow_blank=True
    )
