from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from taskite.permissions import (
    WorkspaceAdminPermission,
    WorkspaceCollaboratorPermission,
)
from taskite.mixins import WorkspaceMixin
from taskite.models.workspace import WorkspaceInvite
from taskite.exceptions import (
    WorkspaceInviteNotFoundException,
)
from taskite.tasks import send_member_invitation_email
from taskite.api.workspace_invites.serializers import (
    WorkspaceInviteSerializer,
    WorkspaceInviteCreateSerializer,
)
from taskite.throttles import ResendEmailThrottle
from taskite.exceptions import InvalidInputException


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
            WorkspaceInvite.objects.filter(
                workspace=request.workspace, confirmed_at__isnull=True
            )
            .select_related("invited_by")
            .order_by("-created_at")
        )
        serializer = WorkspaceInviteSerializer(workspace_invites, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        create_serializer = WorkspaceInviteCreateSerializer(data=request.data)
        if not create_serializer.is_valid():
            raise InvalidInputException

        data = create_serializer.validated_data
        emails = request.data.get("emails")
        # if not emails:
        #     return Response(
        #         data={"detail": "No emails found"}, status=status.HTTP_400_BAD_REQUEST
        #     )

        # invites = []
        # for email in emails:
        #     invite = WorkspaceInvite.objects.create(
        #         workspace=request.workspace, email=email, invited_by=request.user
        #     )
        #     send_member_invitation_email.delay(invite.id)
        #     invites.append(invite)

        # serializer = WorkspaceInviteSerializer(invites, many=True)

        # return Response(
        #     data=serializer.data,
        #     status=status.HTTP_200_OK,
        # )

        return Response(data={"detail": "Ok"})

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

    @action(
        methods=["POST"],
        detail=True,
        url_path="resend-invitation",
        permission_classes=[IsAuthenticated, WorkspaceAdminPermission],
        throttle_classes=[ResendEmailThrottle],
    )
    def resend_invitation(self, request, *args, **kwargs):
        workspace_invite = WorkspaceInvite.objects.filter(
            workspace=request.workspace, id=kwargs.get("pk"), confirmed_at__isnull=True
        ).first()
        if not workspace_invite:
            raise WorkspaceInviteNotFoundException

        send_member_invitation_email.delay(workspace_invite.id)
        message = f"Workspace invite has been sent to {workspace_invite.email}."
        return Response(data={"detail": message}, status=status.HTTP_200_OK)
