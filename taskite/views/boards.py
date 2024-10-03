from django.views import View
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from taskite.models import Workspace, WorkspaceMembership, Board, BoardMembership
from taskite.serializers import WorkspaceSerializer, ProfileSerializer, BoardSerializer


class BoardsView(LoginRequiredMixin, View):
    def get(self, request, workspace_slug):
        workspace = Workspace.objects.filter(slug=workspace_slug).first()
        if not workspace:
            raise Http404

        workspace_membership = WorkspaceMembership.objects.filter(
            workspace=workspace, user=request.user
        ).first()
        if not workspace_membership:
            raise Http404

        context = {
            "props": {
                "workspace": WorkspaceSerializer(workspace).data,
                "current_user": ProfileSerializer(request.user).data,
                "membership_role": workspace_membership.role,
            }
        }
        return render(request, "workspaces/boards/index.html", context)


class BoardsKanbanView(LoginRequiredMixin, View):
    def get(self, request, workspace_slug, board_slug):
        workspace = Workspace.objects.filter(slug=workspace_slug).first()
        if not workspace:
            raise Http404

        workspace_membership = WorkspaceMembership.objects.filter(
            workspace=workspace, user=request.user
        ).first()
        if not workspace_membership:
            raise Http404

        board = Board.objects.filter(slug=board_slug, workspace=workspace).first()
        if not board:
            raise Http404

        # Check for board collaborative permission
        board_permission_queryset = BoardMembership.objects.filter(board=board).filter(
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
        if not board_permission_queryset.exists():
            raise Http404

        context = {
            "props": {
                "workspace": WorkspaceSerializer(workspace).data,
                "board": BoardSerializer(board).data,
                "current_user": ProfileSerializer(request.user).data
            }
        }
        return render(request, "workspaces/boards/kanban.html", context)


class BoardsTableView(LoginRequiredMixin, View):
    def get(self, request, workspace_slug, board_slug):
        workspace = Workspace.objects.filter(slug=workspace_slug).first()
        if not workspace:
            raise Http404

        workspace_membership = WorkspaceMembership.objects.filter(
            workspace=workspace, user=request.user
        ).first()
        if not workspace_membership:
            raise Http404

        board = Board.objects.filter(slug=board_slug, workspace=workspace).first()
        if not board:
            raise Http404

        # Check for board collaborative permission
        board_permission_queryset = BoardMembership.objects.filter(board=board).filter(
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
        if not board_permission_queryset.exists():
            raise Http404

        context = {
            "props": {
                "workspace": WorkspaceSerializer(workspace).data,
                "board": BoardSerializer(board).data,
            }
        }
        return render(request, "workspaces/boards/table.html", context)


class BoardsSettingsGeneralView(LoginRequiredMixin, View):
    def get(self, request, workspace_slug, board_slug):
        workspace = Workspace.objects.filter(slug=workspace_slug).first()
        if not workspace:
            raise Http404

        workspace_membership = WorkspaceMembership.objects.filter(
            workspace=workspace, user=request.user
        ).first()
        if not workspace_membership:
            raise Http404

        board = Board.objects.filter(slug=board_slug, workspace=workspace).first()
        if not board:
            raise Http404

        # Check for board collaborative permission
        board_permission_queryset = BoardMembership.objects.filter(board=board).filter(
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
        if not board_permission_queryset.exists():
            raise Http404
        
        has_edit_permission = False
        is_board_admin_queryset = BoardMembership.objects.filter(board=board).filter(
            Q(user=request.user, role=BoardMembership.Role.ADMIN)
            | Q(team__members=request.user, role=BoardMembership.Role.ADMIN)
        )

        if workspace_membership.role == WorkspaceMembership.Role.ADMIN:
            has_edit_permission = True
        else:
            has_edit_permission = is_board_admin_queryset.exists()

        context = {
            "props": {
                "workspace": WorkspaceSerializer(workspace).data,
                "board": BoardSerializer(board).data,
                "has_edit_permission": has_edit_permission,
            }
        }
        return render(request, "workspaces/boards/settings/general.html", context)


class BoardsSettingsCollaboratorsView(LoginRequiredMixin, View):
    def get(self, request, workspace_slug, board_slug):
        workspace = Workspace.objects.filter(slug=workspace_slug).first()
        if not workspace:
            raise Http404

        workspace_membership = WorkspaceMembership.objects.filter(
            workspace=workspace, user=request.user
        ).first()
        if not workspace_membership:
            raise Http404

        board = Board.objects.filter(slug=board_slug, workspace=workspace).first()
        if not board:
            raise Http404

        # Check for board collaborative permission
        board_permission_queryset = BoardMembership.objects.filter(board=board).filter(
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
        if not board_permission_queryset.exists():
            raise Http404
        
        has_edit_permission = False
        is_board_admin_queryset = BoardMembership.objects.filter(board=board).filter(
            Q(user=request.user, role=BoardMembership.Role.ADMIN)
            | Q(team__members=request.user, role=BoardMembership.Role.ADMIN)
        )

        if workspace_membership.role == WorkspaceMembership.Role.ADMIN:
            has_edit_permission = True
        else:
            has_edit_permission = is_board_admin_queryset.exists()

        context = {
            "props": {
                "workspace": WorkspaceSerializer(workspace).data,
                "board": BoardSerializer(board).data,
                "has_edit_permission": has_edit_permission
            }
        }
        return render(request, "workspaces/boards/settings/collaborators.html", context)
