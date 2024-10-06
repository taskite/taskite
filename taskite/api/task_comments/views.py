from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from taskite.mixins import BoardMixin
from taskite.permissions import BoardCollaboratorPermission
from taskite.models import TaskComment, Task
from taskite.exceptions import TaskNotFoundException
from taskite.api.task_comments.serializers import TaskCommentSerializer


class TaskCommentsViewSet(BoardMixin, ViewSet):
    permission_classes = [IsAuthenticated, BoardCollaboratorPermission]

    def list(self, request, *args, **kwargs):
        task = Task.objects.filter(id=kwargs.get("task_id")).first()
        if not task:
            raise TaskNotFoundException

        comments = TaskComment.objects.filter(task=task).select_related("author")
        serializer = TaskCommentSerializer(comments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
