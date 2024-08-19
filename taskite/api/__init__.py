from rest_framework.routers import SimpleRouter

from taskite.api.accounts.views import AccountsViewSet
from taskite.api.organizations.views import OrganizationViewSet
from taskite.api.boards.views import BoardsViewSet
from taskite.api.states.views import StatesViewSet

router = SimpleRouter(trailing_slash=False, use_regex_path=False)

router.register('accounts', AccountsViewSet, basename='accounts')
router.register('organizations', OrganizationViewSet, basename='organization')
router.register('boards', BoardsViewSet, basename='board')
router.register('boards/<uuid:board_id>/states', StatesViewSet, basename='state')

urlpatterns = router.urls