from django.db import transaction
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from taskite.utils import get_object_or_raise_api_404
from taskite.models import (
    Task,
    TaskAssignee,
    State,
    Priority,
    User,
    TaskComment,
    BoardPermissionRole,
)
from taskite.mixins import BoardMixin
from taskite.api.tasks.serializers import (
    TaskSerializer,
    TaskSequenceUpdateSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
)
from taskite.permissions import BoardGenericPermission
from taskite.exceptions import (
    InvalidInputException,
    TaskNotFoundException,
    StateNotFoundException,
    PriorityNotFoundException,
)


class TasksViewSet(BoardMixin, ViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        match self.action:
            case "list":
                return [IsAuthenticated(), BoardGenericPermission()]
            case "create":
                return [
                    IsAuthenticated(),
                    BoardGenericPermission(
                        allowed_roles=[
                            BoardPermissionRole.ADMIN,
                            BoardPermissionRole.COLLABORATOR,
                            BoardPermissionRole.MAINTAINER,
                        ]
                    ),
                ]
            case "retrieve":
                return [IsAuthenticated(), BoardGenericPermission()]
            case "partial_update":
                return [
                    IsAuthenticated(),
                    BoardGenericPermission(
                        allowed_roles=[
                            BoardPermissionRole.ADMIN,
                            BoardPermissionRole.COLLABORATOR,
                            BoardPermissionRole.MAINTAINER,
                        ]
                    ),
                ]
            case "update_sequence":
                return [
                    IsAuthenticated(),
                    BoardGenericPermission(
                        allowed_roles=[
                            BoardPermissionRole.ADMIN,
                            BoardPermissionRole.MAINTAINER,
                        ]
                    ),
                ]
            case _:
                return super().get_permissions()

    def create(self, request, *args, **kwargs):
        create_serializer = TaskCreateSerializer(data=request.data)
        if not create_serializer.is_valid():
            print(create_serializer.errors)
            raise InvalidInputException

        data = create_serializer.validated_data
        # Check for stateId
        if not State.objects.filter(
            board=request.board, id=data.get("state_id")
        ).exists():
            raise StateNotFoundException

        if (
            data.get("priority_id")
            and not Priority.objects.filter(
                board=request.board, id=data.get("priority_id")
            ).exists()
        ):
            raise PriorityNotFoundException

        assignees = data.pop("assignees")
        task = Task(**data, created_by=request.user, board=request.board)
        task.save()
        if assignees:
            task.assignees.set(assignees)

        serializer = TaskSerializer(task)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        task = Task.objects.filter(board=request.board, id=kwargs.get("pk")).first()
        if not task:
            raise TaskNotFoundException

        serializer = TaskSerializer(task)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        parent_id = request.query_params.get("parent_id", None)
        queryset = Task.objects.filter(
            board=request.board, archived_at__isnull=True, parent_id=parent_id
        )
        if request.query_params.getlist("assignees[]"):
            # Filter for assignees
            assignees = request.query_params.getlist("assignees[]")
            queryset = queryset.filter(assignees__in=assignees)

        if request.query_params.getlist("task_types[]"):
            # Filter for task type
            task_types = request.query_params.getlist("task_types[]")
            queryset = queryset.filter(task_type__in=task_types)

        if request.query_params.getlist("priorities[]"):
            # Filter form priorities
            priorities = request.query_params.getlist("priorities[]")
            queryset = queryset.filter(priority__in=priorities)

        if request.query_params.getlist("labels[]"):
            # Filter for labels
            labels = request.query_params.getlist("labels[]")
            queryset = queryset.filter(labels__in=labels)

        tasks = (
            queryset.prefetch_related("assignees", "labels")
            .select_related("priority", "created_by")
            .order_by("sequence")
        )
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        update_serializer = TaskUpdateSerializer(data=request.data)
        if not update_serializer.is_valid():
            raise InvalidInputException

        task = get_object_or_raise_api_404(
            Task, board=request.board, id=kwargs.get("pk"), message="Task not found."
        )

        data = update_serializer.validated_data

        assignees = None
        if data.get("assignees"):
            assignees = data.pop("assignees")
        for key, value in data.items():
            if key == "priority_id":
                priority = Priority.objects.filter(
                    board=request.board, id=value
                ).first()
                TaskComment.objects.create(
                    task=task,
                    content=f"updated priority to {priority.name}.",
                    author=request.user,
                    comment_type=TaskComment.CommentType.ACTIVITY,
                )

            if key == "task_type":
                TaskComment.objects.create(
                    task=task,
                    content=f"updated task type to {value}.",
                    author=request.user,
                    comment_type=TaskComment.CommentType.ACTIVITY,
                )

            if key == "state_id":
                state = State.objects.filter(board=request.board, id=value).first()
                TaskComment.objects.create(
                    task=task,
                    content=f"updated state to {state.name}.",
                    author=request.user,
                    comment_type=TaskComment.CommentType.ACTIVITY,
                )

            if key == "description":
                TaskComment.objects.create(
                    task=task,
                    content="updated the description.",
                    author=request.user,
                    comment_type=TaskComment.CommentType.ACTIVITY,
                )

            if key == "summary":
                TaskComment.objects.create(
                    task=task,
                    content="updated the summary.",
                    author=request.user,
                    comment_type=TaskComment.CommentType.ACTIVITY,
                )

            setattr(task, key, value)
        task.save(update_fields=data.keys())
        if assignees:
            task.assignees.set(assignees)
        serializer = TaskSerializer(task)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=["PATCH"], detail=True, url_path="update-sequence")
    def update_sequence(self, request, *args, **kwargs):
        update_serializer = TaskSequenceUpdateSerializer(data=request.data)
        if not update_serializer.is_valid():
            raise InvalidInputException
        task = get_object_or_raise_api_404(
            Task, board=request.board, id=kwargs.get("pk")
        )
        data = update_serializer.validated_data

        if data.get("previous_task") and data.get("next_task"):
            previous_task = get_object_or_raise_api_404(
                Task, board=request.board, id=data.get("previous_task")
            )
            next_task = get_object_or_raise_api_404(
                Task, board=request.board, id=data.get("next_task")
            )
            task.sequence = (previous_task.sequence + next_task.sequence) / 2

        elif data.get("previous_task"):
            previous_task = get_object_or_raise_api_404(
                Task, board=request.board, id=data.get("previous_task")
            )
            task.sequence = previous_task.sequence + 10000

        elif data.get("next_task"):
            next_task = get_object_or_raise_api_404(
                Task, board=request.board, id=data.get("next_task")
            )
            task.sequence = next_task.sequence / 2

        task.state_id = data.get("state_id")
        task.save(update_fields=["state_id", "sequence"])
        return Response(
            data={"detail": "Task sequence updated", "new_sequence": task.sequence},
            status=status.HTTP_200_OK,
        )
