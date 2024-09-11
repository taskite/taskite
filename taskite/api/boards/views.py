from django.db.models import Q
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from taskite.models import Board, Workspace, BoardMembership, WorkspaceMembership, User
from taskite.api.boards.serializers import (
    BoardSerializer,
    BoardMembershipSerializer,
    BoardCreateSerializer,
    BoardMemberSeralizer,
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
        return WorkspaceMembership.objects.filter(
            workspace=workspace, user=user
        ).first()

    def check_for_workspace_admin_membership(self, user, workspace):
        permission_queryset = WorkspaceMembership.objects.filter(
            user=user, workspace=workspace, role=WorkspaceMembership.Role.ADMIN
        )
        if not permission_queryset.exists():
            raise WorkspaceInvalidPermission

    def check_for_board_permission(self, user, board):
        # Check for workspace permission
        workspace_membership = self.get_workspace_membership(user, board.workspace)
        if not workspace_membership:
            raise WorkspaceInvalidPermission

        if workspace_membership.role == WorkspaceMembership.Role.COLLABORATOR:
            board_membership_queryset = BoardMembership.objects.filter(
                board=board
            ).filter(Q(user=user) | Q(team__members=user))
            if not board_membership_queryset.exists():
                raise BoardInvalidPermission

    def create(self, request, *args, **kwargs):
        create_serializer = BoardCreateSerializer(data=request.data)
        if not create_serializer.is_valid():
            raise InvalidInputException

        data = create_serializer.validated_data
        workspace_id = data.pop("workspace_id")

        workspace = Workspace.objects.filter(id=workspace_id).first()
        if not workspace:
            raise WorkspaceNotFoundException

        # Check for workspace membership permission
        self.check_for_workspace_admin_membership(request.user, workspace)

        board = Board(**data)
        board.workspace = workspace
        board.created_by = request.user
        board.save()

        serializer = BoardSerializer(board)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        boards = Board.objects.filter(
            Q(
                workspace__memberships__user=request.user,
                workspace__memberships__role=WorkspaceMembership.Role.ADMIN,
            )
            | Q(memberships__user=request.user)
            | Q(memberships__team__members=request.user)
        ).distinct()
        serializer = BoardSerializer(boards, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        board = Board.objects.filter(id=kwargs.get("pk")).first()
        if not board:
            raise BoardNotFoundException

        self.check_for_board_permission(request.user, board)

        serializer = BoardSerializer(board)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=True)
    def membership(self, request, *args, **kwargs):
        board = Board.objects.filter(id=kwargs.get("pk")).first()
        if not board:
            raise BoardNotFoundException

        # Check for workspace permission
        workspace = board.workspace
        workspace_membership = WorkspaceMembership.objects.filter(
            user=request.user, workspace=workspace
        ).first()
        if not workspace_membership:
            raise WorkspaceInvalidPermission

        board_membership = BoardMembership.objects.filter(
            board=board, user=request.user
        ).first()
        if not board_membership:
            raise BoardInvalidPermission

        serializer = BoardMembershipSerializer(board_membership)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=True)
    def members(self, request, *args, **kwargs):
        board = Board.objects.filter(id=kwargs.get("pk")).first()
        if not board:
            raise BoardNotFoundException

        self.check_for_board_permission(request.user, board)

        members = User.objects.filter(
            Q(boards=board) | Q(teams__boards=board)
        ).distinct()

        serializer = BoardMemberSeralizer(members, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
