from django.urls import path
from taskite.views.boards import (
    BoardKanbanView,
    BoardTableView,
    BoardSettingsGeneralView,
    BoardSettingsCollaboratorsView
)

# fmt: off
urlpatterns = [
    path("table/", BoardTableView.as_view(), name="board-table"),
    path("settings/", BoardSettingsGeneralView.as_view(), name="board-settings-general"),
    path("settings/collaborators/", BoardSettingsCollaboratorsView.as_view(), name="board-settings-collaborators"),
    path("", BoardKanbanView.as_view(), name="board-kanban"),
]
