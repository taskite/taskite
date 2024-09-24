from django.db import transaction
from django.utils.crypto import get_random_string
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
from taskite.models import WorkspaceInvite, User
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
        emails = data.get("emails")

        existing_workspace_emails = User.objects.filter(
            workspace_memberships__workspace=request.workspace
        ).values_list("email", flat=True)
        emails = [email for email in emails if email not in existing_workspace_emails]

        with transaction.atomic():
            workspace_invites = []
            for email in emails:
                workspace_invites.append(
                    WorkspaceInvite(
                        workspace=request.workspace,
                        email=email,
                        invitation_id=get_random_string(64),
                        invited_by=request.user,
                    )
                )

            created_invites = WorkspaceInvite.objects.bulk_create(workspace_invites)

        for invite in created_invites:
            send_member_invitation_email.delay(invite.id)

        serializer = WorkspaceInviteSerializer(created_invites, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
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
