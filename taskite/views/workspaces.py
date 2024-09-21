from django.shortcuts import render
from django.views import View
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin

from taskite.models import WorkspaceMembership, Workspace, Team
from taskite.serializers import WorkspaceSerializer, ProfileSerializer, TeamSerializer


class WorkspaceDashboardView(LoginRequiredMixin, View):
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
                "membership_role": workspace_membership.role,
                "current_user": ProfileSerializer(request.user).data,
            }
        }
        return render(request, "workspaces/dashboard.html", context)


class WorkspaceMembersView(LoginRequiredMixin, View):
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
                "membership_role": workspace_membership.role,
                "current_user": ProfileSerializer(request.user).data,
            }
        }
        return render(request, "workspaces/settings/members.html", context)


class WorkspaceTeamsView(LoginRequiredMixin, View):
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
                "membership_role": workspace_membership.role,
                "current_user": ProfileSerializer(request.user).data,
            }
        }
        return render(request, "workspaces/settings/teams/index.html", context)


class WorkspaceTeamsEditView(LoginRequiredMixin, View):
    def get(self, request, workspace_slug, team_id):
        workspace = Workspace.objects.filter(slug=workspace_slug).first()
        if not workspace:
            raise Http404

        workspace_membership = WorkspaceMembership.objects.filter(
            workspace=workspace, user=request.user, role=WorkspaceMembership.Role.ADMIN
        ).first()
        if not workspace_membership:
            raise Http404

        team = Team.objects.filter(workspace=workspace, id=team_id).first()
        if not team:
            raise Http404

        context = {
            "props": {
                "workspace": WorkspaceSerializer(workspace).data,
                "current_user": ProfileSerializer(request.user).data,
                "team": TeamSerializer(team).data,
            }
        }
        return render(request, "workspaces/settings/teams/edit.html", context)


class WorkspaceSettingsGeneralView(LoginRequiredMixin, View):
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
        return render(request, "workspaces/settings/general.html", context)


class WorkspaceSettingsBillingView(LoginRequiredMixin, View):
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
        return render(request, "workspaces/settings/billing.html", context)
