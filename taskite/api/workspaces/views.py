from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from taskite.models.workspace import Workspace, WorkspaceMembership
from taskite.api.workspaces.serializers import (
    WorkspaceSerializer,
    WorkspaceMembershipSerializer,
)
from taskite.exceptions import WorkspaceNotFoundException


class WorkspaceViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        workspaces = Workspace.objects.filter(memberships__user=request.user)
        serializer = WorkspaceSerializer(workspaces, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        workspace = Workspace.objects.filter(
            memberships__user=request.user, id=kwargs.get("pk")
        ).first()
        if not workspace:
            raise WorkspaceNotFoundException

        serializer = WorkspaceSerializer(workspace)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def memberships(self, request, *args, **kwargs):
        memberships = WorkspaceMembership.objects.filter(user=request.user)
        serializer = WorkspaceMembershipSerializer(memberships, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
