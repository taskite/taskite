from django.views import View
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin

from taskite.models import WorkspaceMembership, Board, Sprint
from taskite.serializers import (
    WorkspaceSerializer,
    ProfileSerializer,
    BoardSerializer,
    SprintSerializer,
)
from taskite.mixins import BoardPermissionMixin


class BoardKanbanView(LoginRequiredMixin, BoardPermissionMixin, View):
    def get(self, request, board_slug):
        board = get_object_or_404(Board, slug=board_slug)

        if not self.has_valid_board_permission(board, request.user):
            raise Http404

        context = {
            "props": {
                "workspace": WorkspaceSerializer(board.workspace).data,
                "board": BoardSerializer(board).data,
                "current_user": ProfileSerializer(request.user).data,
            }
        }
        return render(request, "boards/kanban.html", context)


class BoardTableView(LoginRequiredMixin, BoardPermissionMixin, View):
    def get(self, request, board_slug):
        board = get_object_or_404(Board, slug=board_slug)

        if not self.has_valid_board_permission(board, request.user):
            raise Http404

        context = {
            "props": {
                "workspace": WorkspaceSerializer(board.workspace).data,
                "board": BoardSerializer(board).data,
            }
        }
        return render(request, "boards/table.html", context)


class BoardSettingsGeneralView(LoginRequiredMixin, BoardPermissionMixin, View):
    def get(self, request, board_slug):
        board = get_object_or_404(Board, slug=board_slug)

        if not self.has_valid_board_permission(board, request.user):
            raise Http404

        # Check permission
        has_edit_permission = self.has_valid_board_permission(
            board, request.user, allowed_roles=["admin", "maintainer"]
        )

        context = {
            "props": {
                "workspace": WorkspaceSerializer(board.workspace).data,
                "board": BoardSerializer(board).data,
                "has_edit_permission": has_edit_permission,
            }
        }
        return render(request, "boards/settings/general.html", context)


class BoardSettingsCollaboratorsView(LoginRequiredMixin, BoardPermissionMixin, View):
    def get(self, request, board_slug):
        board = get_object_or_404(Board, slug=board_slug)

        if not self.has_valid_board_permission(board, request.user):
            raise Http404

        # Check permission
        has_edit_permission = self.has_valid_board_permission(
            board, request.user, allowed_roles=["admin", "maintainer"]
        )

        context = {
            "props": {
                "workspace": WorkspaceSerializer(board.workspace).data,
                "board": BoardSerializer(board).data,
                "has_edit_permission": has_edit_permission,
            }
        }
        return render(request, "boards/settings/collaborators.html", context)


class BoardSettingsStatesView(LoginRequiredMixin, BoardPermissionMixin, View):
    def get(self, request, board_slug):
        board = get_object_or_404(Board, slug=board_slug)

        if not self.has_valid_board_permission(board, request.user):
            raise Http404

        # Check permission
        has_edit_permission = self.has_valid_board_permission(
            board, request.user, allowed_roles=["admin", "maintainer"]
        )

        context = {
            "props": {
                "workspace": WorkspaceSerializer(board.workspace).data,
                "board": BoardSerializer(board).data,
                "has_edit_permission": has_edit_permission,
            }
        }
        return render(request, "boards/settings/states.html", context)
