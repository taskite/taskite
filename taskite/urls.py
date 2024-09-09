from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from taskite.views import (
    InviteWorkspaceConfirmView,
    InviteWorkspaceRejectView,
    AccountVerificationView,
)

# fmt: off
urlpatterns = [
    path("api/", include("taskite.api")),
    path("admin/", admin.site.urls),
    path("invites/workspace/<uuid:invite_id>/confirm/", InviteWorkspaceConfirmView.as_view(), name="invite-workspace-confirm"),
    path("invites/workspace/<uuid:invite_id>/reject/", InviteWorkspaceRejectView.as_view(), name="invite-workspace-reject"),
    path("accounts/verification/<str:verification_id>/", AccountVerificationView.as_view(), name="account-verification"),
    re_path(r"^.*$", TemplateView.as_view(template_name="ui/index.html"), name="root"), 
]
