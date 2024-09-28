from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from taskite.views.home import (
    IndexView,
    CreateView,
    FileUploadView
)

# fmt: off
urlpatterns = [
    re_path(r'^upload/(?P<file_key>.*)$', FileUploadView.as_view(), name="file-upload"),
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