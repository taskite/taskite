from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from calyvim.api.teams.serializers import TeamSerializer, TeamCreateSerializer
from calyvim.exceptions import InvalidInputException, TeamNotFoundException
from calyvim.models.team import Team
from calyvim.mixins import WorkspaceMixin
from calyvim.permissions import WorkspaceGenericPermission


class TeamsViewSet(WorkspaceMixin, ViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        match self.action:
            case "list":
                return [
                    IsAuthenticated(),
                    WorkspaceGenericPermission(),
                ]
            case "create":
                return [
                    IsAuthenticated(),
                    WorkspaceGenericPermission(allowed_roles=["admin", "maintainer"]),
                ]
            case "destroy":
                return [
                    IsAuthenticated(),
                    WorkspaceGenericPermission(allowed_roles=["admin", "maintainer"]),
                ]

            case "search":
                return [
                    IsAuthenticated(),
                    WorkspaceGenericPermission(),
                ]

            case _:
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

    @action(methods=["GET"], detail=False)
    def search(self, request, *args, **kwargs):
        query = request.query_params.get("q")
        if not query:
            return Response(
                data={"detail": "Please enter search query."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        teams = request.workspace.teams.filter(name__icontains=query)
        serializer = TeamSerializer(teams, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
