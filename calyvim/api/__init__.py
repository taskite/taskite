from rest_framework.routers import SimpleRouter

from calyvim.api.accounts.views import AccountsViewSet
from calyvim.api.boards.views import BoardViewSet
from calyvim.api.workspaces.views import WorkspaceViewSet
from calyvim.api.states.views import StatesViewSet
from calyvim.api.tasks.views import TasksViewSet
from calyvim.api.priorities.views import PrioritiesViewSet
from calyvim.api.workspace_memberships.views import WorkspaceMembershipsViewset
from calyvim.api.teams.views import TeamsViewSet
from calyvim.api.workspace_invites.views import WorkspaceInvitesViewSet
from calyvim.api.team_memberships.views import TeamMembershipsViewSet
from calyvim.api.uploads.views import UploadsViewSet
from calyvim.api.task_comments.views import TaskCommentsViewSet
from calyvim.api.labels.views import LabelsViewSet
from calyvim.api.board_permissions.views import BoardPermissionsViewSet
from calyvim.api.board_team_permissions.views import BoardTeamPermissionsViewSet
from calyvim.api.task_attachments.views import TaskAttachementsViewSet
from calyvim.api.newslines.views import NewslinesViewSet
from calyvim.api.estimates.views import EstimatesViewSets
from calyvim.api.sprints.views import SprintsViewSet

router = SimpleRouter(trailing_slash=False, use_regex_path=False)

# fmt: off
# Uploads
router.register("uploads", UploadsViewSet, basename="upload")

# Accounts
router.register("accounts", AccountsViewSet, basename="accounts")

# Workspaces
router.register("workspaces/<uuid:workspace_id>/memberships", WorkspaceMembershipsViewset, basename="workspace-membership")
router.register("workspaces/<uuid:workspace_id>/invites", WorkspaceInvitesViewSet, basename="workspace-invite")
router.register("workspaces/<uuid:workspace_id>/teams", TeamsViewSet, basename="team")
router.register("workspaces/<uuid:workspace_id>/team_memberships", TeamMembershipsViewSet, basename="team-membership")
router.register("workspaces", WorkspaceViewSet, basename="workspace")

# Boards
router.register("boards", BoardViewSet, basename="board")
router.register("boards/<uuid:board_id>/states", StatesViewSet, basename="state")
router.register("boards/<uuid:board_id>/tasks", TasksViewSet, basename="task")
router.register("boards/<uuid:board_id>/tasks/<uuid:task_id>/comments", TaskCommentsViewSet, basename="task-comment")
router.register("boards/<uuid:board_id>/tasks/<uuid:task_id>/attachments", TaskAttachementsViewSet, basename="task-attachment")
router.register("boards/<uuid:board_id>/priorities", PrioritiesViewSet, basename="priority")
router.register("boards/<uuid:board_id>/labels", LabelsViewSet, basename="label")
router.register("boards/<uuid:board_id>/permissions", BoardPermissionsViewSet, basename="board-permission")
router.register("boards/<uuid:board_id>/team_permissions", BoardTeamPermissionsViewSet, basename="board-team-permission")
router.register("boards/<uuid:board_id>/estimates", EstimatesViewSets, basename="estimate")
router.register("boards/<uuid:board_id>/sprints", SprintsViewSet, basename="sprint")

# Newslines
router.register("newslines", NewslinesViewSet, basename="newsline")

urlpatterns = router.urls
