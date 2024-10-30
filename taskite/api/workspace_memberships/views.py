from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from taskite.mixins import WorkspaceMixin
from taskite.permissions import WorkspaceGenericPermission
from taskite.models.workspace import WorkspaceMembership
from taskite.exceptions import (
    WorkspaceMembershipNotFoundException,
    InvalidInputException,
)
from taskite.api.workspace_memberships.serializers import (
    WorkspaceMembershipSerializer,
    WorkspaceMembershipUpdateSerializer,
)


class WorkspaceMembershipsViewset(WorkspaceMixin, ViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        match self.action:
            case "list":
                return [
                    IsAuthenticated(),
                    WorkspaceGenericPermission(
                        allowed_roles=["admin", "maintainer", "collaborator", "guest"]
                    ),
                ]
            case "destroy":
                return [
                    IsAuthenticated(),
                    WorkspaceGenericPermission(allowed_roles=["admin", "maintainer"]),
                ]
            case "partial_update":
                return [
                    IsAuthenticated(),
                    WorkspaceGenericPermission(allowed_roles=["admin", "maintainer"]),
                ]
            case _:
                return super().get_permissions()

    def list(self, request, *args, **kwargs):
        workspace_memberships = (
            WorkspaceMembership.objects.filter(workspace=request.workspace)
            .select_related("user")
            .prefetch_related("user__teams")
        )
        serializer = WorkspaceMembershipSerializer(workspace_memberships, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        workspace_membership = WorkspaceMembership.objects.filter(
            workspace=request.workspace, id=kwargs.get("pk")
        ).first()

        if not workspace_membership:
            raise WorkspaceMembershipNotFoundException

        workspace_membership.delete()
        return Response(
            data={"detail": "Workspace membership got deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )

    def partial_update(self, request, *args, **kwargs):
        workspace_membership = WorkspaceMembership.objects.filter(
            workspace=request.workspace, id=kwargs.get("pk")
        ).first()

        if not workspace_membership:
            raise WorkspaceMembershipNotFoundException

        update_serializer = WorkspaceMembershipUpdateSerializer(data=request.data)
        if not update_serializer.is_valid():
            raise InvalidInputException

        data = update_serializer.validated_data
        for key, value in data.items():
            setattr(workspace_membership, key, value)

        workspace_membership.save(update_fields=data.keys())
        serializer = WorkspaceMembershipSerializer(workspace_membership)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
