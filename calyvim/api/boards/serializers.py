from rest_framework import serializers

from calyvim.mixins import NameAndSourceSerializerMixin
from calyvim.models import User, Board, Task


class BoardCreateSerializer(serializers.Serializer):
    workspace_id = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    template_id = serializers.UUIDField(required=False, allow_null=True)


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


class BoardMemberSeralizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "display_name",
            "avatar",
        ]


class TaskSerializer(serializers.ModelSerializer):
    board = BoardSerializer()

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "board_id",
            "board",
            "task_type",
            "summary",
            "created_at",
        ]
