from django.urls import path
from taskite.views.boards import (
    BoardsView,
    BoardsKanbanView,
    BoardsTableView,
    BoardsSettingsGeneralView,
    BoardsSettingsCollaboratorsView
)

# fmt: off
urlpatterns = [
    path("<str:board_slug>/", BoardsKanbanView.as_view(), name="workspaces-boards-kanban"),
    path("<str:board_slug>/table/", BoardsTableView.as_view(), name="workspaces-boards-table"),
    path("<str:board_slug>/settings/", BoardsSettingsGeneralView.as_view(), name="workspaces-boards-settings-general"),
    path("<str:board_slug>/settings/collaborators/", BoardsSettingsCollaboratorsView.as_view(), name="workspaces-boards-settings-collaborators"),
    path("", BoardsView.as_view(), name="workspaces-boards"),
]
