from rest_framework import permissions
from taskite.models import WorkspaceMembership


class WorkspaceAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        queryset = WorkspaceMembership.objects.filter(
            workspace=request.workspace,
            user=request.user,
            role=WorkspaceMembership.Role.ADMIN,
        )
        return queryset.exists()


class WorkspaceCollaboratorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        queryset = WorkspaceMembership.objects.filter(
            workspace=request.workspace,
            user=request.user,
            role__in=[
                WorkspaceMembership.Role.ADMIN,
                WorkspaceMembership.Role.COLLABORATOR,
            ],
        )
        return queryset.exists()


class WorkspaceGenericPermission(permissions.BasePermission):
    def __init__(self, allowed_roles=WorkspaceMembership.Role.values):
        self.allowed_roles = allowed_roles

    def has_permission(self, request, view):
        queryset = WorkspaceMembership.objects.filter(
            workspace=request.workspace, user=request.user, role__in=self.allowed_roles
        )
        return queryset.exists()
