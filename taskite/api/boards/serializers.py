from rest_framework import serializers

from taskite.models.board import Board, BoardMembership
from taskite.models.user import User


class BoardCreateSerializer(serializers.Serializer):
    workspace_id = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["id", "name", "slug", "description", "created_at"]


class BoardMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardMembership
        fields = ["id", "board_id", "role", "created_at"]


class BoardMemberSeralizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
        ]
