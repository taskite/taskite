from rest_framework import serializers

from taskite.mixins import NameAndSourceSerializerMixin
from taskite.models.board import Board, BoardMembership
from taskite.models.user import User


class BoardCreateSerializer(serializers.Serializer):
    workspace_id = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["id", "name", "slug", "cover", "description", "created_at"]


class BoardDetailSerializer(NameAndSourceSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = [
            "id",
            "name",
            "slug",
            "cover",
            "task_prefix",
            "description",
            "created_at",
        ]


class BoardUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    cover = serializers.CharField(required=False, allow_null=True)
    slug = serializers.CharField(required=False)
    task_prefix = serializers.CharField(required=False)
    description = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )


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
