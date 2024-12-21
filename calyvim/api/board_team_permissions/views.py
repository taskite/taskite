from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from calyvim.models import BoardTeamPermission
from calyvim.permissions import (
    BoardCollaboratorPermission,
    BoardAdminPermission,
    BoardGenericPermission,
)
from calyvim.mixins import BoardMixin
from calyvim.api.board_team_permissions.serializers import (
    BoardTeamPermissionSerializer,
    BoardTeamCreateSerializer,
    BoardTeamPermissionUpdateSerializer,
)
from calyvim.exceptions import (
    InvalidInputException,
    BoardTeamPermissionNotFoundException,
)


class BoardTeamPermissionsViewSet(BoardMixin, ViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        match self.action:
            case "list":
                return [IsAuthenticated(), BoardGenericPermission()]
            case "create":
                return [
                    IsAuthenticated(),
                    BoardGenericPermission(allowed_roles=["admin", "maintainer"]),
                ]
            case "partial_update":
                return [
                    IsAuthenticated(),
                    BoardGenericPermission(allowed_roles=["admin", "maintainer"]),
                ]
            case "destroy":
                return [
                    IsAuthenticated(),
                    BoardGenericPermission(allowed_roles=["admin", "maintainer"]),
                ]
            case _:
                return super().get_permissions()
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        create_serializer = BoardTeamCreateSerializer(data=request.data)
        if not create_serializer.is_valid():
            raise InvalidInputException

        data = create_serializer.validated_data
        existing_team_permission_queryset = BoardTeamPermission.objects.filter(
            board=request.board, team__id=data.get("team_id")
        )
        if existing_team_permission_queryset.exists():
            return Response(
                data={"detail": "Team already has permission."},
                status=status.HTTP_403_FORBIDDEN,
            )
        permission = BoardTeamPermission.objects.create(board=request.board, **data)
        serializer = BoardTeamPermissionSerializer(permission)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        permissions = BoardTeamPermission.objects.filter(
            board=request.board
        ).select_related("team")
        serializer = BoardTeamPermissionSerializer(permissions, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        update_serializer = BoardTeamPermissionUpdateSerializer(data=request.data)
        if not update_serializer.is_valid():
            raise InvalidInputException

        permission = BoardTeamPermission.objects.filter(
            id=kwargs.get("pk"), board=request.board
        ).first()
        if not permission:
            BoardTeamPermissionNotFoundException

        data = update_serializer.validated_data
        for key, value in data.items():
            setattr(permission, key, value)
        permission.save(update_fields=data.keys())
        serializer = BoardTeamPermissionSerializer(permission)
        return Response(
            data={
                "detail": "Board team permission udpated successfully.",
                "permission": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        permission = BoardTeamPermission.objects.filter(
            id=kwargs.get("pk"), board=request.board
        ).first()
        if not permission:
            BoardTeamPermissionNotFoundException

        permission.delete()
        return Response(
            data={"detail": "Team Permission got deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
