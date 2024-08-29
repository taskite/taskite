from rest_framework.routers import SimpleRouter

from taskite.api.accounts.views import AccountsViewSet
from taskite.api.boards.views import BoardViewSet
from taskite.api.workspaces.views import WorkspaceViewSet
from taskite.api.states.views import StatesViewSet
from taskite.api.tasks.views import TasksViewSet
from taskite.api.priorities.views import PrioritiesViewSet

router = SimpleRouter(trailing_slash=False, use_regex_path=False)

router.register("accounts", AccountsViewSet, basename="accounts")
router.register("workspaces", WorkspaceViewSet, basename="workspace")
router.register("boards", BoardViewSet, basename="board")
router.register("boards/<uuid:board_id>/states", StatesViewSet, basename="state")
router.register("boards/<uuid:board_id>/tasks", TasksViewSet, basename="task")
router.register("boards/<uuid:board_id>/priorities", PrioritiesViewSet, basename="priority")

urlpatterns = router.urls
