from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView
from taskite.views import IndexView

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(
        r"^dashboard/.*$", TemplateView.as_view(template_name="dashboard/index.html")
    ),
    path("", IndexView.as_view(), name="index"), 
]
