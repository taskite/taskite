from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from taskite.views import IndexView, InviteWorkspaceConfirmView, AccountVerificationView

# fmt: off
urlpatterns = [
    path("api/", include("taskite.api")),
    path("admin/", admin.site.urls),
    re_path(r"^dashboard/.*$", TemplateView.as_view(template_name="dashboard/index.html"), name="dashboard"),
    path("invites/workspace/<uuid:invite_id>/confirm/", InviteWorkspaceConfirmView.as_view(), name="invite-workspace-confirm"),
    path("accounts/verification/<str:verification_id>/", AccountVerificationView.as_view(), name="account-verification"),
    path("", IndexView.as_view(), name="index"), 
]
