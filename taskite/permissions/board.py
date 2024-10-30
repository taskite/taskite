from rest_framework import permissions

from taskite.models import WorkspaceMembership, BoardPermission, BoardPermissionRole


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


class BoardGenericPermission(permissions.BasePermission):
    def __init__(self, allowed_roles=BoardPermissionRole.values):
        self.allowed_roles = allowed_roles

    def has_permission(self, request, view):
        # Check for workspace permission for admin roles
        workspace_membership = WorkspaceMembership.objects.filter(
            user=request.user, workspace=request.board.workspace
        ).first()
        if not workspace_membership:
            return False

        if workspace_membership.role == WorkspaceMembership.Role.ADMIN:
            return True

        # Check for board memberships
        board_permission_queryset = BoardPermission.objects.filter(
            user=request.user, board=request.board, role__in=self.allowed_roles
        )

        return board_permission_queryset.exists()
