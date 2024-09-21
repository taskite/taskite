from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import Http404, HttpResponseServerError
from django.db import transaction
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import serializers

from taskite.models import User, WorkspaceInvite, WorkspaceMembership, Workspace, Team
from taskite.serializers import WorkspaceSerializer, ProfileSerializer, TeamSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "username"]


class LoginView(View):
    def get(self, request):
        next = request.GET.get("next", "/")
        context = {
            "props": {
                "next": next,
            }
        }
        return render(request, "accounts/login.html", context)


class RegisterView(View):
    def get(self, request):
        return render(request, "accounts/register.html")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("accounts-login")


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        workspace = request.user.workspaces.first()

        return redirect("workspaces-dashboard", workspace_slug=workspace.slug)


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


class WorkspaceBoardsView(View):
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


class InviteWorkspaceConfirmView(View):
    def get(self, request, invite_id):
        invite = WorkspaceInvite.objects.filter(id=invite_id, accepted=False).first()
        if not invite:
            raise Http404

        user = User.objects.filter(email=invite.email).first()
        if not user:
            redirect_path = (
                settings.APP_URL
                + "/dashboard/accounts/register"
                + f"?email={invite.email}&inviteId={invite.id}"
            )
            return redirect(redirect_path)

        # Check for existing Membership
        queryset = WorkspaceMembership.objects.filter(
            user=user, workspace=invite.workspace
        )

        if queryset.exists():
            raise Http404

        try:
            with transaction.atomic():
                WorkspaceMembership.objects.create(
                    user=user,
                    workspace=invite.workspace,
                    role=WorkspaceMembership.Role.COLLABORATOR,
                )
                invite.accepted = True
                invite.save()
        except:
            raise HttpResponseServerError

        login(request, user)
        return redirect(f"{settings.APP_URL}" + reverse("dashboard"))


class InviteWorkspaceRejectView(View):
    def get(self, request, invite_id):
        invite = WorkspaceInvite.objects.filter(id=invite_id, accepted=False).first()
        if not invite:
            raise Http404

        invite.delete()
        if request.user.is_authenticated:
            return redirect(f"{settings.APP_URL}" + reverse("dashboard"))

        return redirect("index")


class AccountVerificationView(View):
    def get(self, request, verification_id):
        user = User.objects.filter(verification_id=verification_id).first()
        if not user:
            raise Http404

        user.verify()
        login(request, user)
        return redirect(f"{settings.APP_URL}" + reverse("dashboard"))
