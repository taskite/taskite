from django.db.models import Q
from rest_framework import permissions

from taskite.models import WorkspaceMembership, BoardMembership, Workspace


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
        board_permission_queryset = BoardMembership.objects.filter(
            board=request.board
        ).filter(
            Q(
                user=request.user,
                role__in=[
                    BoardMembership.Role.ADMIN,
                    BoardMembership.Role.COLLABORATOR,
                ],
            )
            | Q(
                team__members=request.user,
                role__in=[
                    BoardMembership.Role.ADMIN,
                    BoardMembership.Role.COLLABORATOR,
                ],
            )
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
        board_permission_queryset = BoardMembership.objects.filter(
            board=request.board
        ).filter(
            Q(user=request.user, role=BoardMembership.Role.ADMIN)
            | Q(team__members=request.user, role=BoardMembership.Role.ADMIN)
        )
        return board_permission_queryset.exists()
