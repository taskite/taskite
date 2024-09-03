from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from taskite.api.teams.serializers import TeamSerializer
from taskite.models.team import Team
from taskite.models.workspace import Workspace
from taskite.exceptions import WorkspaceNotFoundException


class TeamsViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        workspace = Workspace.objects.filter(id=kwargs.get("workspace_id")).first()
        if not workspace:
            raise WorkspaceNotFoundException

        teams = Team.objects.filter(workspace=workspace).prefetch_related("members")
        serializer = TeamSerializer(teams, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
