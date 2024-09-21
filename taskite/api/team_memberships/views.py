from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from taskite.models import TeamMembership, Team
from taskite.api.team_memberships.serializers import (
    TeamMembershipSerializer,
    TeamMembershipCreateSerializer,
)
from taskite.permissions import WorkspaceAdminPermission
from taskite.mixins import WorkspaceMixin
from taskite.exceptions import (
    TeamNotFoundException,
    InvalidInputException,
    MemberNotFoundException,
    TeamMembershipNotFoundEception,
)


class TeamMembershipsViewSet(WorkspaceMixin, ViewSet):
    permission_classes = [IsAuthenticated, WorkspaceAdminPermission]

    def list(self, request, *args, **kwargs):
        team_id = request.query_params.get("team_id")
        if not team_id:
            return Response(
                data={"detail": "Please provide team id."}, status=status.HTTP_200_OK
            )

        team = Team.objects.filter(id=team_id, workspace=request.workspace).first()
        if not team:
            raise TeamNotFoundException

        team_memberships = TeamMembership.objects.filter(team=team).prefetch_related(
            "user"
        )
        serializer = TeamMembershipSerializer(team_memberships, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        create_serializer = TeamMembershipCreateSerializer(data=request.data)
        if not create_serializer.is_valid():
            raise InvalidInputException

        data = create_serializer.validated_data

        team_id = data.get("team_id")
        team = Team.objects.filter(id=team_id, workspace=request.workspace).first()
        if not team:
            raise TeamNotFoundException

        member_id = data.get("member_id")
        user = request.workspace.members.filter(id=member_id).first()
        if not user:
            raise MemberNotFoundException

        existing_membership_queryset = TeamMembership.objects.filter(
            user=user, team=team
        )
        if existing_membership_queryset.exists():
            return Response(
                data={"detail": "Member is already a part of the team"},
                status=status.HTTP_403_FORBIDDEN,
            )

        team_membership = TeamMembership.objects.create(user=user, team=team)
        serializer = TeamMembershipSerializer(team_membership)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        membership = TeamMembership.objects.filter(id=kwargs.get("pk")).first()
        if not membership:
            raise TeamMembershipNotFoundEception

        user = membership.user
        membership.delete()

        return Response(
            data={"detail": f"{user.first_name} is removed from the team."},
            status=status.HTTP_204_NO_CONTENT,
        )
