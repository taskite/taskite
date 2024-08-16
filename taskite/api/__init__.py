from rest_framework.routers import SimpleRouter

from taskite.api.accounts.views import AccountsViewSet
from taskite.api.organizations.views import OrganizationViewSet

router = SimpleRouter(trailing_slash=False, use_regex_path=False)

router.register('accounts', AccountsViewSet, basename='accounts')
router.register('organizations', OrganizationViewSet, basename='organization')

urlpatterns = router.urls