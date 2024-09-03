from rest_framework.routers import SimpleRouter

from taskite.api.accounts.views import AccountsViewSet
from taskite.api.boards.views import BoardViewSet
from taskite.api.workspaces.views import WorkspaceViewSet
from taskite.api.states.views import StatesViewSet
from taskite.api.tasks.views import TasksViewSet
from taskite.api.priorities.views import PrioritiesViewSet
from taskite.api.workspace_memberships.views import WorkspaceMembershipsViewset
from taskite.api.teams.views import TeamsViewSet
from taskite.api.workspace_invites.views import WorkspaceInvitesViewSet

router = SimpleRouter(trailing_slash=False, use_regex_path=False)

# fmt: off

# Accounts
router.register("accounts", AccountsViewSet, basename="accounts")

# Workspaces
router.register("workspaces/<uuid:workspace_id>/memberships", WorkspaceMembershipsViewset, basename="workspace-membership")
router.register("workspaces/<uuid:workspace_id>/invites", WorkspaceInvitesViewSet, basename="workspace-invite")
router.register("workspaces/<uuid:workspace_id>/teams", TeamsViewSet, basename="team")
router.register("workspaces", WorkspaceViewSet, basename="workspace")

# Boards
router.register("boards", BoardViewSet, basename="board")
router.register("boards/<uuid:board_id>/states", StatesViewSet, basename="state")
router.register("boards/<uuid:board_id>/tasks", TasksViewSet, basename="task")
router.register("boards/<uuid:board_id>/priorities", PrioritiesViewSet, basename="priority")

urlpatterns = router.urls
