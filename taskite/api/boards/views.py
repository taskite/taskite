from django.db.models import F, Value
from django.db.models.functions import Concat
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from taskite.utils import update_file_field, get_object_or_raise_api_404
from taskite.models import (
    Board,
    Workspace,
    BoardPermission,
    WorkspaceMembership,
    User,
    Task,
    BoardPermission,
    BoardPermissionRole,
)
from taskite.api.boards.serializers import (
    BoardSerializer,
    BoardCreateSerializer,
    BoardMemberSeralizer,
    BoardDetailSerializer,
    BoardUpdateSerializer,
    TaskSerializer,
)
from taskite.exceptions import (
    InvalidInputException,
    WorkspaceNotFoundException,
    WorkspaceInvalidPermission,
    BoardNotFoundException,
    BoardInvalidPermission,
)


class BoardViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def get_workspace_membership(self, user, workspace):
        workspace_membership = get_object_or_raise_api_404(
            WorkspaceMembership, user=user, workspace=workspace
        )
        return workspace_membership

    def check_for_board_permission(
        self, user, board, allowed_roles=BoardPermissionRole.values
    ):
        # Check if user has membership in the workspace related to the board
        workspace_membership = self.get_workspace_membership(user, board.workspace)
        if not workspace_membership:
            raise WorkspaceInvalidPermission

        # Allow access if the user is an admin or maintainer in the workspace
        if workspace_membership.role in {
            WorkspaceMembership.Role.ADMIN,
            WorkspaceMembership.Role.MAINTAINER,
        }:
            return

        # Check if user has specific board permission if not an admin or maintainer
        has_permission = BoardPermission.objects.filter(
            user=user, board=board, role__in=allowed_roles
        ).exists()
        if not has_permission:
            raise BoardInvalidPermission

    def check_for_workspace_roles(
        self, user, workspace, allowed_roles=WorkspaceMembership.Role.values
    ):
        queryset = WorkspaceMembership.objects.filter(
            workspace=workspace, user=user, role__in=allowed_roles
        )
        return queryset.exists()

    def create(self, request, *args, **kwargs):
        create_serializer = BoardCreateSerializer(data=request.data)
        if not create_serializer.is_valid():
            raise InvalidInputException

        data = create_serializer.validated_data
        workspace = get_object_or_raise_api_404(
            Workspace, id=data.pop("workspace_id"), message="Workspace not found."
        )

        # Check for workspace membership permission
        self.check_for_workspace_roles(
            request.user, workspace, ["admin", "collaborator", "maintainer"]
        )

        board = Board(**data)
        board.workspace = workspace
        board.created_by = request.user
        board.save()

        serializer = BoardSerializer(board)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        workspace_id = request.query_params.get("workspace_id")
        if not workspace_id:
            raise InvalidInputException

        workspace = get_object_or_raise_api_404(Workspace, id=workspace_id)

        workspace_membership = self.get_workspace_membership(
            request.user, workspace=workspace
        )

        if workspace_membership.role == WorkspaceMembership.Role.ADMIN:
            boards = Board.objects.filter(workspace=workspace)
        else:
            boards = (
                Board.objects.filter(workspace=workspace)
                .filter(permissions__user=request.user)
                .distinct()
            )
        serializer = BoardSerializer(boards, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        board = get_object_or_raise_api_404(
            Board, id=kwargs.get("pk"), message="Board not found."
        )

        self.check_for_board_permission(request.user, board)

        serializer = BoardDetailSerializer(board)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        board = get_object_or_raise_api_404(
            Board, id=kwargs.get("pk"), message="Board not found."
        )

        self.check_for_board_permission(request.user, board, ["admin", "maintainer"])

        update_serializer = BoardUpdateSerializer(data=request.data)
        if not update_serializer.is_valid():
            raise InvalidInputException

        data = update_serializer.validated_data
        update_tasks_prefix = False

        if "cover" in data:
            update_file_field(board, "cover", data.get("cover"))

        if data.get("task_prefix") and data.get("task_prefix") != board.task_prefix:
            # Check if task prefix is getting updated
            update_tasks_prefix = True

        for key, value in data.items():
            setattr(board, key, value)

        board.save(update_fields=data.keys())

        if update_tasks_prefix:
            Task.objects.filter(board=board).update(
                name=Concat(Value(board.task_prefix), Value("-"), F("number"))
            )

        serializer = BoardDetailSerializer(board)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=True)
    def members(self, request, *args, **kwargs):
        board = get_object_or_raise_api_404(
            Board, id=kwargs.get("pk"), message="Board not found."
        )
        self.check_for_board_permission(request.user, board)
        members = (
            User.objects.filter(user_board_permissions__board=board)
            .distinct()
            .order_by("first_name")
        )

        serializer = BoardMemberSeralizer(members, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def stats(self, request, *args, **kwargs):
        workspace_id = request.query_params.get("workspace_id")
        if not workspace_id:
            raise InvalidInputException

        workspace = Workspace.objects.filter(id=workspace_id).first()
        if not workspace:
            raise WorkspaceNotFoundException

        workspace_membership = WorkspaceMembership.objects.filter(
            workspace=workspace, user=request.user
        ).first()
        if not workspace_membership:
            raise WorkspaceInvalidPermission

        if workspace_membership.role == WorkspaceMembership.Role.ADMIN:
            boards = Board.objects.filter(workspace=workspace)
        else:
            boards = (
                Board.objects.filter(workspace=workspace)
                .filter(permissions__user=request.user)
                .distinct()
            )

        created_tasks_count = Task.objects.filter(
            board__in=boards, created_by=request.user
        ).count()

        assigned_tasks_count = Task.objects.filter(
            board__in=boards, task_assignees__user=request.user
        ).count()

        recent_tasks_created = Task.objects.filter(
            board__in=boards, created_by=request.user
        ).select_related("board")[:5]
        recent_tasks_assigned = Task.objects.filter(
            board__in=boards, task_assignees__user=request.user
        ).select_related("board")[:5]

        data = {
            "created_tasks_count": created_tasks_count,
            "assigned_tasks_count": assigned_tasks_count,
            "recent_tasks_created": TaskSerializer(
                recent_tasks_created, many=True
            ).data,
            "recent_tasks_assigned": TaskSerializer(
                recent_tasks_assigned, many=True
            ).data,
        }
        return Response(data=data, status=status.HTTP_200_OK)
