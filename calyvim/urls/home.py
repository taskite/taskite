from django.urls import path

from calyvim.views.home import IndexView, TermsView

urlpatterns = [
    path("terms/", TermsView.as_view(), name="home-terms"),
    path("", IndexView.as_view(), name="home-index"),
]