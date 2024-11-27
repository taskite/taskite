from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from taskite.mixins import BoardMixin
from taskite.permissions import BoardGenericPermission
from taskite.api.task_attachments.serializers import (
    TaskAttachmentCreateSerializer,
    TaskAttachmentSerializer,
)
from taskite.exceptions import InvalidInputException
from taskite.utils import get_object_or_raise_api_404
from taskite.models import Task, TaskAttachment
from taskite.tasks import file_promote


class TaskAttachementsViewSet(BoardMixin, ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        task = get_object_or_raise_api_404(Task, id=kwargs.get("task_id"))
        attachments = TaskAttachment.objects.filter(task=task)
        serializer = TaskAttachmentSerializer(attachments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        create_serializer = TaskAttachmentCreateSerializer(data=request.data)
        if not create_serializer.is_valid():
            raise InvalidInputException

        task = get_object_or_raise_api_404(Task, id=kwargs.get("task_id"))
        data = create_serializer.validated_data
        attachment = TaskAttachment(**data, task=task)
        attachment.save()
        file_promote.delay(data.get("attachment"))

        serializer = TaskAttachmentSerializer(attachment)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
