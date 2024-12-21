from django.urls import path

from calyvim.views.accounts import (
    LoginView,
    RegisterView,
    LogoutView,
    VerifyView,
    VerifyConfirmView,
    ProfileView,
    ResetView,
    ResetConfirmView,
    SecurityView
)

# fmt: off
urlpatterns = [
    path("login/", LoginView.as_view(), name="accounts-login"),
    path("register/", RegisterView.as_view(), name="accounts-register"),
    path("logout/", LogoutView.as_view(), name="accounts-logout"),
    path("verify/", VerifyView.as_view(), name="accounts-verify"),
    path("verify/<str:verification_id>/confirm/", VerifyConfirmView.as_view(), name="accounts-verify-confirm"),
    path("profile/", ProfileView.as_view(), name="accounts-profile"),
    path("reset/", ResetView.as_view(), name="accounts-reset"),
    path("reset/<str:password_reset_id>/confirm/", ResetConfirmView.as_view(), name="accounts-reset-confirm"),
    path("security/", SecurityView.as_view(), name="accounts-security")
]
