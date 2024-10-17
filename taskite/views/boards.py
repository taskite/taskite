from django.views import View
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from taskite.models import (
    WorkspaceMembership,
    Board,
)
from taskite.serializers import WorkspaceSerializer, ProfileSerializer, BoardSerializer
from taskite.mixins import PermissionCheckMixin


class BoardKanbanView(LoginRequiredMixin, PermissionCheckMixin, View):
    def get(self, request, board_slug):
        board = get_object_or_404(Board, slug=board_slug)

        self.check_for_workspace_permission(board.workspace, request.user)
        self.check_for_board_permission(board, request.user)

        context = {
            "props": {
                "workspace": WorkspaceSerializer(board.workspace).data,
                "board": BoardSerializer(board).data,
                "current_user": ProfileSerializer(request.user).data,
            }
        }
        return render(request, "boards/kanban.html", context)


class BoardTableView(LoginRequiredMixin, PermissionCheckMixin, View):
    def get(self, request, board_slug):
        board = get_object_or_404(Board, slug=board_slug)

        self.check_for_workspace_permission(board.workspace, request.user)
        self.check_for_board_permission(board, request.user)

        context = {
            "props": {
                "workspace": WorkspaceSerializer(board.workspace).data,
                "board": BoardSerializer(board).data,
            }
        }
        return render(request, "boards/table.html", context)


class BoardSettingsGeneralView(LoginRequiredMixin, PermissionCheckMixin, View):
    def get(self, request, board_slug):
        board = get_object_or_404(Board, slug=board_slug)

        # Check and get workspace membership permission
        workspace_membership = self.check_and_get_workpace_permssion(
            board.workspace, request.user
        )

        # Check for board-level permission
        self.check_for_board_permission(board, request.user)

        # Check board-edit permission
        has_edit_permission = (
            workspace_membership.role == WorkspaceMembership.Role.ADMIN
            or self.has_board_admin_permission(board, request.user)
        )

        context = {
            "props": {
                "workspace": WorkspaceSerializer(board.workspace).data,
                "board": BoardSerializer(board).data,
                "has_edit_permission": has_edit_permission,
            }
        }
        return render(request, "boards/settings/general.html", context)


class BoardSettingsCollaboratorsView(LoginRequiredMixin, PermissionCheckMixin, View):
    def get(self, request, board_slug):
        board = get_object_or_404(Board, slug=board_slug)

        # Check and get workspace membership permission
        workspace_membership = self.check_and_get_workpace_permssion(
            board.workspace, request.user
        )

        # Check for board-level permission
        self.check_for_board_permission(board, request.user)

        # Check board-edit permission
        has_edit_permission = (
            workspace_membership.role == WorkspaceMembership.Role.ADMIN
            or self.has_board_admin_permission(board, request.user)
        )

        context = {
            "props": {
                "workspace": WorkspaceSerializer(board.workspace).data,
                "board": BoardSerializer(board).data,
                "has_edit_permission": has_edit_permission,
            }
        }
        return render(request, "boards/settings/collaborators.html", context)
