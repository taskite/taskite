from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from taskite.models.workspace import Workspace, WorkspaceMembership, WorkspaceInvite
from taskite.exceptions import WorkspaceNotFoundException
from taskite.api.workspace_memberships.serializers import WorkspaceMembershipSerializer
from taskite.tasks.workspace import workspace_invite_confirm


class WorkspaceMembershipsViewset(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        workspace = Workspace.objects.filter(id=kwargs.get("workspace_id")).first()
        if not workspace:
            raise WorkspaceNotFoundException

        workspace_memberships = (
            WorkspaceMembership.objects.filter(workspace=workspace)
            .select_related("user")
            .prefetch_related("user__teams")
        )
        serializer = WorkspaceMembershipSerializer(workspace_memberships, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def invite(self, request, *args, **kwargs):
        workspace = Workspace.objects.filter(id=kwargs.get("workspace_id")).first()
        if not workspace:
            raise WorkspaceNotFoundException

        emails = request.data.get("emails")
        if not emails:
            return Response(
                data={"detail": "No emails found"}, status=status.HTTP_400_BAD_REQUEST
            )

        for email in emails:
            invite = WorkspaceInvite.objects.create(
                workspace=workspace, email=email, invited_by=request.user
            )
            workspace_invite_confirm.delay(invite.id)

        return Response(
            data={
                "detail": "Invitations and notifications has been sent to join the workspace"
            },
            status=status.HTTP_200_OK,
        )