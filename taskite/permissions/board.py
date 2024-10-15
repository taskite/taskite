from rest_framework import permissions

from taskite.models import (
    WorkspaceMembership,
    BoardPermission,
)


class BoardCollaboratorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        workspace = request.board.workspace

        # Check for workspace permission
        workspace_membership = WorkspaceMembership.objects.filter(
            workspace=workspace,
            user=request.user,
            role__in=[
                WorkspaceMembership.Role.ADMIN,
                WorkspaceMembership.Role.COLLABORATOR,
            ],
        ).first()

        if workspace_membership.role == WorkspaceMembership.Role.ADMIN:
            return True

        # Check for board collaborative permission
        board_permission_queryset = BoardPermission.objects.filter(
            board=request.board, user=request.user, role__in=["admin", "collaborator"]
        )
        return board_permission_queryset.exists()


class BoardAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        workspace = request.board.workspace

        # Check for workspace permission
        workspace_membership = WorkspaceMembership.objects.filter(
            workspace=workspace,
            user=request.user,
            role__in=[
                WorkspaceMembership.Role.ADMIN,
                WorkspaceMembership.Role.COLLABORATOR,
            ],
        ).first()

        if workspace_membership.role == WorkspaceMembership.Role.ADMIN:
            return True

        # Check for board collaborative permission
        board_permission_queryset = BoardPermission.objects.filter(
            board=request.board, user=request.user, role="admin"
        )
        return board_permission_queryset.exists()
