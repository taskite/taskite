from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from taskite.api.teams.serializers import TeamSerializer, TeamCreateSerializer
from taskite.exceptions import InvalidInputException, TeamNotFoundException
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

    def create(self, request, *args, **kwargs):
        create_serializer = TeamCreateSerializer(data=request.data)
        if not create_serializer.is_valid():
            raise InvalidInputException

        data = create_serializer.data
        team = Team.objects.create(**data, workspace=request.workspace)
        serializer = TeamSerializer(team)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        team = Team.objects.filter(id=kwargs.get("pk")).first()
        if not team:
            raise TeamNotFoundException

        team.delete()
        return Response(
            data={"detail": "Team deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
