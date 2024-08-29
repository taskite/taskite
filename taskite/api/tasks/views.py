from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from taskite.models import Task
from taskite.mixins import BoardMixin
from taskite.api.tasks.serializers import TaskSerializer
from taskite.permissions import BoardPermission


class TasksViewSet(BoardMixin, ViewSet):
    permission_classes = [IsAuthenticated, BoardPermission]

    def list(self, request, *args, **kwargs):
        tasks = Task.objects.filter(board=request.board).prefetch_related("assignees")
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
