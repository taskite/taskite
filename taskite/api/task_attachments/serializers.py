from rest_framework import serializers

from taskite.models import TaskAttachment, User, TaskComment


class TaskAttachmentCreateSerializer(serializers.Serializer):
    attachment = serializers.CharField()
    filename = serializers.CharField()


class TaskAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAttachment
        fields = ["id", "attachment", "created_at"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "display_name",
            "last_name",
            "avatar",
        ]


class TaskCommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = TaskComment
        fields = ["id", "content", "author", "comment_type", "created_at"]
