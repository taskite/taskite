from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from calyvim.views.extras import FileUploadView, UpView

# fmt: off
urlpatterns = [
    re_path(r'^upload/(?P<file_key>.*)$', FileUploadView.as_view(), name="file-upload"),
    path("up/", UpView.as_view(), name="up"),
    path("api/", include("calyvim.api")),
    path("admin/", admin.site.urls),
    path("app/accounts/", include("calyvim.urls.accounts")),
    path("app/b/<uuid:board_id>/", include("calyvim.urls.boards")),
    path("app/", include("calyvim.urls.workspaces")),
    path("", include("calyvim.urls.home")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
