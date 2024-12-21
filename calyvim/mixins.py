from rest_framework import serializers
from django.http import Http404

from calyvim.models import (
    Board,
    Workspace,
    WorkspaceMembership,
    BoardPermission,
    BoardPermissionRole,
)
from calyvim.exceptions import BoardNotFoundException, WorkspaceNotFoundException
from calyvim.utils import get_object_or_404


class FileUploadMixin:
    def save(self, *args, **kwargs):
        # Call the original save() method to actually save the instance
        super().save(*args, **kwargs)


class BoardMixin:
    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)
        board_id = kwargs.get("board_id")
        if board_id:
            board = Board.objects.filter(id=board_id).first()
            if not board:
                raise BoardNotFoundException
            request.board = board
        return request


class WorkspaceMixin:
    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)
        workspace_id = kwargs.get("workspace_id")
        if workspace_id:
            workspace = Workspace.objects.filter(id=workspace_id).first()
            if not workspace:
                raise WorkspaceNotFoundException
            request.workspace = workspace
        return request


class FileNameAndSourceSerializerMixin:
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field_name, field in self.fields.items():
            if isinstance(field, serializers.FileField):
                field_value = getattr(instance, field_name)
                if field_value:
                    # Set the original field to the filename
                    representation[field_name] = field_value.name
                    # Add a new field with 'Src' suffix containing the URL
                    representation[f"{field_name}_src"] = field_value.url
                else:
                    # If the field is empty, set both fields to None
                    representation[field_name] = None
                    representation[f"{field_name}_src"] = None
        return representation


class NameAndSourceSerializerMixin:
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field_name, field in self.fields.items():
            if isinstance(field, serializers.FileField):
                field_value = getattr(instance, field_name)
                if field_value:
                    # Set the original field to the filename
                    representation[field_name] = field_value.name
                    # Add a new field with 'Src' suffix containing the URL
                    representation[f"{field_name}_src"] = field_value.url
                else:
                    # If the field is empty, set both fields to None
                    representation[field_name] = None
                    representation[f"{field_name}_src"] = None
        return representation


class PermissionCheckMixin:
    def check_for_workspace_permission(self, workspace, user):
        workspace_membership_queryset = WorkspaceMembership.objects.filter(
            workspace=workspace, user=user
        )
        if not workspace_membership_queryset.exists():
            raise Http404

    def check_for_board_permission(self, board, user):
        board_permission_queryset = BoardPermission.objects.filter(
            board=board, user=user, role__in=["admin", "collaborator"]
        )
        if not board_permission_queryset.exists():
            raise Http404

    def check_and_get_workpace_permssion(self, workspace, user):
        workspace_membership = WorkspaceMembership.objects.filter(
            workspace=workspace, user=user
        ).first()

        if not workspace_membership:
            raise Http404

        return workspace_membership

    def has_board_admin_permission(self, board, user):
        permission_queryset = BoardPermission.objects.filter(
            board=board, user=user, role="admin"
        )
        return permission_queryset.exists()


class WorkspacePermissionMixin:
    def has_valid_permission(
        self, workspace, user, allowed_roles=WorkspaceMembership.Role.values
    ):
        permission_queryset = WorkspaceMembership.objects.filter(
            workspace=workspace, user=user, role__in=allowed_roles
        )
        return permission_queryset.exists()

    def has_valid_membership(self, workspace, user):
        membership_queryset = WorkspaceMembership.objects.filter(
            workspace=workspace, user=user
        )
        return membership_queryset.exists()


class BoardPermissionMixin:
    def get_workspace_membership(self, workspace, user):
        workspace_membership = get_object_or_404(
            WorkspaceMembership, workspace=workspace, user=user
        )
        return workspace_membership

    def has_valid_board_permission(
        self, board, user, allowed_roles=BoardPermissionRole.values
    ):
        membership = self.get_workspace_membership(board.workspace, user)
        if membership.role == WorkspaceMembership.Role.ADMIN:
            return True

        permission_queryset = BoardPermission.objects.filter(
            user=user, board=board, role__in=allowed_roles
        )
        return permission_queryset.exists()
