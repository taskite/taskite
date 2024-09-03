from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from taskite.models.workspace import Workspace, WorkspaceMembership, WorkspaceInvite
from taskite.exceptions import WorkspaceNotFoundException
from taskite.api.workspace_memberships.serializers import WorkspaceMembershipSerializer
from taskite.tasks.workspace import workspace_invite_confirm
from taskite.api.workspace_invites.serializers import WorkspaceInviteSerializer


class WorkspaceInvitesViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        workspace = Workspace.objects.filter(id=kwargs.get("workspace_id")).first()
        if not workspace:
            raise WorkspaceNotFoundException

        workspace_invites = WorkspaceInvite.objects.filter(
            workspace=workspace, accepted=False
        ).select_related("invited_by").order_by("-created_at")
        serializer = WorkspaceInviteSerializer(workspace_invites, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        workspace = Workspace.objects.filter(id=kwargs.get("workspace_id")).first()
        if not workspace:
            raise WorkspaceNotFoundException

        emails = request.data.get("emails")
        if not emails:
            return Response(
                data={"detail": "No emails found"}, status=status.HTTP_400_BAD_REQUEST
            )

        invites = []
        for email in emails:
            invite = WorkspaceInvite.objects.create(
                workspace=workspace, email=email, invited_by=request.user
            )
            workspace_invite_confirm.delay(invite.id)
            invites.append(invite)

        serializer = WorkspaceInviteSerializer(invites, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
