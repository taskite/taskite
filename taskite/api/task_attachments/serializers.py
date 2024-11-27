from rest_framework import serializers

from taskite.models import TaskAttachment


class TaskAttachmentCreateSerializer(serializers.Serializer):
    attachment = serializers.CharField()


class TaskAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAttachment
        fields = ["id", "attachment", "created_at"]
