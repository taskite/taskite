from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from taskite.models import Board, Workspace, BoardMembership, WorkspaceMembership
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
        workspace = (
            Workspace.objects.filter(id=workspace_id)
            .filter(memberships__user=request.user)
            .filter(memberships__role=WorkspaceMembership.Role.ADMIN)
            .first()
        )
        if not workspace:
            raise WorkspaceInvalidPermission

        board = Board(**data)
        board.workspace = workspace
        board.created_by = request.user
        board.save()

        serializer = BoardSerializer(board)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        boards = Board.objects.filter(memberships__user=request.user)
        serializer = BoardSerializer(boards, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
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

        serializer = BoardSerializer(board)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def memberships(self, request, *args, **kwargs):
        memberships = BoardMembership.objects.filter(user=request.user)
        serializer = BoardMembershipSerializer(memberships, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

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

        members = board.members.all()
        serializer = BoardMemberSeralizer(members, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
