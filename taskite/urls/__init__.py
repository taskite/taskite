from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from taskite.views.home import (
    IndexView,
    CreateView
)

# fmt: off
urlpatterns = [
    path("api/", include("taskite.api")),
    path("admin/", admin.site.urls),
    path("accounts/", include("taskite.urls.accounts")),
    path("create/", CreateView.as_view(), name="home-create"),
    path("<str:workspace_slug>/boards/", include("taskite.urls.boards")),
    path("<str:workspace_slug>/", include("taskite.urls.workspaces")),
    path("", IndexView.as_view(), name="home-index")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)