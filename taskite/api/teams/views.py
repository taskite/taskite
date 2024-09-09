from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from taskite.api.teams.serializers import TeamSerializer
from taskite.models.team import Team
from taskite.mixins import WorkspaceMixin
from taskite.permissions import (
    WorkspaceCollaboratorPermission,
    WorkspaceAdminPermission,
)


class TeamsViewSet(WorkspaceMixin, ViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == "list":
            return [IsAuthenticated(), WorkspaceCollaboratorPermission()]
        elif self.action == "create":
            return [IsAuthenticated(), WorkspaceAdminPermission()]
        elif self.action == "destroy":
            return [IsAuthenticated(), WorkspaceAdminPermission()]

        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        teams = Team.objects.filter(workspace=request.workspace).prefetch_related(
            "members"
        )
        serializer = TeamSerializer(teams, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
