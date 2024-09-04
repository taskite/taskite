from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.http import Http404, HttpResponseServerError
from django.db import transaction
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import login

from taskite.models.workspace import WorkspaceInvite, WorkspaceMembership
from taskite.models.user import User


# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, "index.html")


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
