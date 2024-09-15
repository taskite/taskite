from django.contrib import admin
from django.urls import path, include
from taskite.views import (
    InviteWorkspaceConfirmView,
    InviteWorkspaceRejectView,
    AccountVerificationView,
    IndexView, 
    LoginView,
    RegisterView,
    LogoutView,
    WorkspaceDashboardView,
    WorkspaceMembersView,
    WorkspaceTeamsView,
    WorkspaceTeamsEditView
)

# fmt: off
urlpatterns = [
    path("api/", include("taskite.api")),
    path("admin/", admin.site.urls),
    path("invites/workspace/<uuid:invite_id>/confirm/", InviteWorkspaceConfirmView.as_view(), name="invite-workspace-confirm"),
    path("invites/workspace/<uuid:invite_id>/reject/", InviteWorkspaceRejectView.as_view(), name="invite-workspace-reject"),
    path("accounts/verification/<str:verification_id>/", AccountVerificationView.as_view(), name="account-verification"),
    path("accounts/login/", LoginView.as_view(), name="accounts-login"),
    path("accounts/register/", RegisterView.as_view(), name="accounts-register"),
    path("accounts/logout/", LogoutView.as_view(), name="accounts-logout"),
    path("<str:workspace_slug>/", WorkspaceDashboardView.as_view(), name="workspaces-dashboard"),
    path("<str:workspace_slug>/members/", WorkspaceMembersView.as_view(), name="workspaces-members"),
    path("<str:workspace_slug>/teams/", WorkspaceTeamsView.as_view(), name="workspaces-teams"),
    path("<str:workspace_slug>/teams/<uuid:team_id>/edit/", WorkspaceTeamsEditView.as_view(), name="workspaces-teams-edit"),
    path("", IndexView.as_view(), name="home-index")
]
