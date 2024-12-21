from django.db.models import F, Value
from django.db.models.functions import Concat
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Count
from django.db.models.functions import TruncDate

from calyvim.utils import update_file_field, get_object_or_raise_api_404
from calyvim.models import (
    Board,
    Workspace,
    BoardPermission,
    WorkspaceMembership,
    User,
    Task,
    BoardPermission,
    BoardPermissionRole,
    TaskAssignee,
)
from calyvim.api.boards.serializers import (
    BoardSerializer,
    BoardCreateSerializer,
    BoardMemberSeralizer,
    BoardDetailSerializer,
    BoardUpdateSerializer,
    TaskSerializer,
)
from calyvim.exceptions import (
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
            print(create_serializer.errors)
            raise InvalidInputException

        data = create_serializer.validated_data
        workspace = get_object_or_raise_api_404(
            Workspace, id=data.pop("workspace_id"), message="Workspace not found."
        )

        # Check for workspace membership permission
        self.check_for_workspace_roles(
            request.user, workspace, ["admin", "collaborator", "maintainer"]
        )

        template_id = data.pop("template_id", None)
        board = Board(**data)
        board.workspace = workspace
        board.created_by = request.user

        if template_id is not None:
            template_board = Board.template_objects.filter(id=template_id).first()
            board.is_from_template = True
            board.template = template_board
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

    @action(methods=["GET"], detail=False, url_path="templates")
    def template(self, request, *args, **kwargs):
        workspace_id = request.query_params.get("workspace_id")
        if not workspace_id:
            raise InvalidInputException

        workspace = get_object_or_raise_api_404(Workspace, id=workspace_id)

        # Checking for workspace membership
        self.check_for_workspace_roles(request.user, workspace)

        template_boards = Board.template_objects.filter()
        serializer = BoardSerializer(template_boards, many=True)

        response_data = {
            "results": serializer.data
        }
        return Response(data=response_data, status=status.HTTP_200_OK)

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

        # Recent Tasks Created
        recent_tasks_created = Task.objects.filter(
            board__in=boards, created_by=request.user
        ).select_related("board")[:5]

        # Recent Task Assigned
        recent_tasks_assigned = Task.objects.filter(
            board__in=boards, task_assignees__user=request.user
        ).select_related("board")[:5]

        # Task Contributions
        task_countributions_count = (
            TaskAssignee.objects.filter(
                user=request.user, created_at__year=2024, task__board__in=boards
            )
            .annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(task_count=Count("task_id"))
            .order_by("day")
        )

        # Format the day field using strftime after retrieving the queryset
        formatted_task_contributions_count = [
            {
                "day": entry["day"].strftime("%Y-%m-%d"),
                "task_count": entry["task_count"],
            }
            for entry in task_countributions_count
        ]

        data = {
            "created_tasks_count": created_tasks_count,
            "assigned_tasks_count": assigned_tasks_count,
            "recent_tasks_created": TaskSerializer(
                recent_tasks_created, many=True
            ).data,
            "recent_tasks_assigned": TaskSerializer(
                recent_tasks_assigned, many=True
            ).data,
            "task_contributions": formatted_task_contributions_count,
        }
        return Response(data=data, status=status.HTTP_200_OK)
