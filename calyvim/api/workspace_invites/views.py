from django.db import transaction
from django.utils.crypto import get_random_string
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from calyvim.permissions import WorkspaceGenericPermission
from calyvim.mixins import WorkspaceMixin
from calyvim.models import WorkspaceInvite, User
from calyvim.exceptions import (
    WorkspaceInviteNotFoundException,
)
from calyvim.tasks import send_member_invitation_email
from calyvim.api.workspace_invites.serializers import (
    WorkspaceInviteSerializer,
    WorkspaceInviteCreateSerializer,
)
from calyvim.throttles import ResendEmailThrottle
from calyvim.exceptions import InvalidInputException


class WorkspaceInvitesViewSet(WorkspaceMixin, ViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        match self.action:
            case "list":
                return [IsAuthenticated(), WorkspaceGenericPermission()]
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

            case "resend_invitation":
                return [
                    IsAuthenticated(),
                    WorkspaceGenericPermission(allowed_roles=["admin", "maintainer"]),
                ]
            case _:
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
