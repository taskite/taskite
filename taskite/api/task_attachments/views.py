from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from taskite.mixins import BoardMixin
from taskite.permissions import BoardGenericPermission
from taskite.api.task_attachments.serializers import (
    TaskAttachmentCreateSerializer,
    TaskAttachmentSerializer,
    TaskCommentSerializer,
)
from taskite.exceptions import InvalidInputException
from taskite.utils import get_object_or_raise_api_404
from taskite.models import Task, TaskAttachment, TaskComment
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
        attachment = TaskAttachment.objects.create(**data, task=task)
        comment = TaskComment.objects.create(
            task=task,
            author=request.user,
            content=f"added {data.get("filename")} as an attachment",
            comment_type=TaskComment.CommentType.ACTIVITY,
        )
        file_promote.delay(data.get("attachment"))

        attachment_serializer = TaskAttachmentSerializer(attachment)
        comment_serializer = TaskCommentSerializer(comment)
        response_data = {
            "attachment": attachment_serializer.data,
            "comment": comment_serializer.data,
        }
        return Response(data=response_data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        task = get_object_or_raise_api_404(Task, id=kwargs.get("task_id"))
        attachment = get_object_or_raise_api_404(
            TaskAttachment, task=task, id=kwargs.get("pk")
        )
        attachment.delete()
        comment = TaskComment.objects.create(
            task=task,
            author=request.user,
            content=f"removed an attachment called {attachment.filename}",
            comment_type=TaskComment.CommentType.ACTIVITY,
        )
        comment_serializer = TaskCommentSerializer(comment)
        response_data = {
            "detail": "Attachment removed successfully",
            "comment": comment_serializer.data,
        }
        return Response(data=response_data, status=status.HTTP_200_OK)
