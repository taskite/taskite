from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from calyvim.mixins import BoardMixin
from calyvim.permissions import BoardGenericPermission
from calyvim.models import TaskComment, Task
from calyvim.exceptions import TaskNotFoundException, InvalidInputException
from calyvim.api.task_comments.serializers import (
    TaskCommentSerializer,
    TaskCommentCreateSerializer,
)
from calyvim.utils import get_object_or_raise_api_404


class TaskCommentsViewSet(BoardMixin, ViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        match self.action:
            case "list":
                return [IsAuthenticated(), BoardGenericPermission()]
            case "create":
                return [IsAuthenticated(), BoardGenericPermission()]
            case _:
                return super().get_permissions()

    def create(self, request, *args, **kwargs):
        create_serializer = TaskCommentCreateSerializer(data=request.data)
        if not create_serializer.is_valid():
            raise InvalidInputException

        task = get_object_or_raise_api_404(Task, id=kwargs.get("task_id"))
        data = create_serializer.validated_data
        comment = TaskComment.objects.create(
            **data,
            author=request.user,
            comment_type=TaskComment.CommentType.UPDATE,
            task=task,
        )
        serializer = TaskCommentSerializer(comment)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        comment_type = request.query_params.get("comment_type", "all")
        task = get_object_or_raise_api_404(Task, id=kwargs.get("task_id"))
        comments = (
            TaskComment.objects.filter(task=task)
            .select_related("author")
            .order_by("-created_at")
        )

        if comment_type != "all":
            comments = comments.filter(comment_type=comment_type)

        serializer = TaskCommentSerializer(comments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def last(self, request, *args, **kwargs):
        task = Task.objects.filter(id=kwargs.get("task_id")).first()
        if not task:
            raise TaskNotFoundException

        comment = TaskComment.objects.filter(task=task).order_by("created_at").last()
        serializer = TaskCommentSerializer(comment)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
