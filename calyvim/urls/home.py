from django.urls import path

from calyvim.views.home import index, terms

urlpatterns = [
    path("terms/", terms, name="home-terms"),
    path("", index, name="home-index"),
]