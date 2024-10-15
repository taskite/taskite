from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from taskite.mixins import BoardMixin
from taskite.models import BoardPermission, WorkspaceMembership
from taskite.permissions import BoardCollaboratorPermission, BoardAdminPermission
from taskite.api.board_permissions.serializers import (
    BoardPermissionSerializer,
    BoardPermissionCreateSerializer,
    BoardPermissionUpdateSerializer,
)
from taskite.exceptions import (
    InvalidInputException,
    WorkspaceMembershipNotFoundException,
    BoardPermissionNotFoundException,
)


class BoardPermissionsViewSet(BoardMixin, ViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == "list":
            return [IsAuthenticated(), BoardCollaboratorPermission()]
        elif self.action == "create":
            return [IsAuthenticated(), BoardAdminPermission()]
        elif self.action == "partial_update":
            return [IsAuthenticated(), BoardAdminPermission()]
        elif self.action == "destroy":
            return [IsAuthenticated(), BoardAdminPermission()]

        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        permissions = BoardPermission.user_objects.filter(
            board=request.board
        ).select_related("user")
        serializer = BoardPermissionSerializer(permissions, many=True)
        return Response(data=serializer.data)

    def create(self, request, *args, **kwargs):
        create_serializer = BoardPermissionCreateSerializer(data=request.data)
        if not create_serializer.is_valid():
            raise InvalidInputException

        data = create_serializer.validated_data
        workspace_membership = WorkspaceMembership.objects.filter(
            workspace=request.board.workspace, user__id=data.get("user_id")
        ).first()
        if not workspace_membership:
            raise WorkspaceMembershipNotFoundException

        existing_permission_queryset = BoardPermission.user_objects.filter(
            user=workspace_membership.user, board=request.board
        )
        if existing_permission_queryset.exists():
            return Response(
                data={"detail": "User already has permission."},
                status=status.HTTP_403_FORBIDDEN,
            )

        permission = BoardPermission.objects.create(
            user=workspace_membership.user,
            board=request.board,
            workspace_membership=workspace_membership,
            role=data.get("role"),
        )
        serializer = BoardPermissionSerializer(permission)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        update_serializer = BoardPermissionUpdateSerializer(data=request.data)
        if not update_serializer.is_valid():
            raise InvalidInputException

        permission = BoardPermission.user_objects.filter(
            id=kwargs.get("pk"), board=request.board
        ).first()
        if not permission:
            BoardPermissionNotFoundException

        data = update_serializer.validated_data
        for key, value in data.items():
            setattr(permission, key, value)
        permission.save(update_fields=data.keys())
        serializer = BoardPermissionSerializer(permission)
        return Response(
            data={
                "detail": "Board permission udpated successfully.",
                "permission": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        permission = BoardPermission.user_objects.filter(
            id=kwargs.get("pk"), board=request.board
        ).first()
        if not permission:
            BoardPermissionNotFoundException

        # Check for atleast 1 board permission
        if BoardPermission.user_objects.filter(board=request.board).count() == 1:
            return Response(
                data={"detail": "You can't remove the default permission."},
                status=status.HTTP_403_FORBIDDEN,
            )

        permission.delete()
        return Response(
            data={"detail": "Permission got deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
