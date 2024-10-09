from django.urls import path

from taskite.views.home import IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="home-index")
]