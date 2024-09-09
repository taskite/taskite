from rest_framework import serializers

from taskite.models import BoardMembership, User, Team


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
        ]


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name", "created_at"]


class BoardMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    team = TeamSerializer()

    class Meta:
        model = BoardMembership
        fields = ["id", "user", "team", "role", "created_at"]
