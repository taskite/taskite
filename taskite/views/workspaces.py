from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.contrib.auth import login

from taskite.models import WorkspaceMembership, Workspace, Team, WorkspaceInvite, User
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


class WorkspaceMemberConfirmationView(View):
    def get(self, request, *args, **kwargs):
        invite = WorkspaceInvite.objects.filter(
            workspace__slug=kwargs.get("workspace_slug"),
            invitation_id=kwargs.get("invitation_id"),
            confirmed_at__isnull=True,
        ).first()

        if not invite:
            raise Http404
        
        # Check for existing user with the invite email
        user = User.objects.filter(email=invite.email).first()
        if not user:
            # Redirect to register page along with invitation ID
            return redirect(reverse('accounts-register') + f"?invitation_id={invite.invitation_id}")
        
        try:
            if not user.is_verified:
                user.verify()

            with transaction.atomic():
                WorkspaceMembership.objects.create(user=user, workspace=invite.workspace)
                invite.confirm_invitation()
        
        except Exception as e:
            print(e)

        login(request, user)
        return redirect('workspaces-dashboard', workspace_slug=invite.workspace.slug)