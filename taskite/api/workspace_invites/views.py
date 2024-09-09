from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from taskite.permissions import (
    WorkspaceAdminPermission,
    WorkspaceCollaboratorPermission,
)
from taskite.mixins import WorkspaceMixin
from taskite.models.workspace import WorkspaceInvite
from taskite.exceptions import (
    WorkspaceInviteNotFoundException,
)
from taskite.tasks.workspace import workspace_invite_confirm
from taskite.api.workspace_invites.serializers import WorkspaceInviteSerializer


class WorkspaceInvitesViewSet(WorkspaceMixin, ViewSet):
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
        workspace_invites = (
            WorkspaceInvite.objects.filter(workspace=request.workspace, accepted=False)
            .select_related("invited_by")
            .order_by("-created_at")
        )
        serializer = WorkspaceInviteSerializer(workspace_invites, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        emails = request.data.get("emails")
        if not emails:
            return Response(
                data={"detail": "No emails found"}, status=status.HTTP_400_BAD_REQUEST
            )

        invites = []
        for email in emails:
            invite = WorkspaceInvite.objects.create(
                workspace=request.workspace, email=email, invited_by=request.user
            )
            workspace_invite_confirm.delay(invite.id)
            invites.append(invite)

        serializer = WorkspaceInviteSerializer(invites, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        workspace_invite = WorkspaceInvite.objects.filter(
            workspace=request.workspace, id=kwargs.get("pk")
        ).first()
        if not workspace_invite:
            raise WorkspaceInviteNotFoundException

        workspace_invite.delete()
        return Response(
            data={"detail": "Workspace invite deleted"}, status=status.HTTP_200_OK
        )
