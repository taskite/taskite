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
        fields = ["id", "name", "avatar", "created_at"]


class BoardMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    team = TeamSerializer()

    class Meta:
        model = BoardMembership
        fields = ["id", "user", "team", "role", "created_at"]


class BoardMembershipCreateSerializer(serializers.Serializer):
    resource_id = serializers.UUIDField()
    role = serializers.ChoiceField(choices=BoardMembership.Role.choices)


class BoardMembershipUpdateSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=BoardMembership.Role.choices)
