from django.urls import path

from taskite.views.accounts import (
    LoginView,
    RegisterView,
    LogoutView,
    VerifyView,
    VerifyConfirmView
)

# fmt: off
urlpatterns = [
    path("login/", LoginView.as_view(), name="accounts-login"),
    path("register/", RegisterView.as_view(), name="accounts-register"),
    path("logout/", LogoutView.as_view(), name="accounts-logout"),
    path("verify/", VerifyView.as_view(), name="accounts-verify"),
    path("verify/<str:verification_id>/confirm/", VerifyConfirmView.as_view(), name="accounts-verify-confirm")
]
