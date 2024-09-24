from django.urls import path
from taskite.views.workspaces import (
    WorkspaceDashboardView,
    WorkspaceMembersView,
    WorkspaceTeamsView,
    WorkspaceTeamsEditView,
    WorkspaceSettingsGeneralView,
    WorkspaceSettingsBillingView,
    WorkspaceMemberConfirmationView
)

# fmt: off
urlpatterns = [
    path("", WorkspaceDashboardView.as_view(), name="workspaces-dashboard"),
    path("settings/", WorkspaceSettingsGeneralView.as_view(), name="workspaces-settings-general"),
    path("settings/billing/", WorkspaceSettingsBillingView.as_view(), name="workspaces-settings-billing"),
    path("settings/members/", WorkspaceMembersView.as_view(), name="workspaces-members"),
    path("settings/teams/", WorkspaceTeamsView.as_view(), name="workspaces-teams"),
    path("settings/teams/<uuid:team_id>/edit/", WorkspaceTeamsEditView.as_view(), name="workspaces-teams-edit"),
    path("members/<str:invitation_id>/confirm/", WorkspaceMemberConfirmationView.as_view(), name="workspaces-member-confirmation")
]
