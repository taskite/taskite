from django.contrib.auth import login, logout
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle

from taskite.api.accounts.serializers import (
    UserSerializer,
    LoginSerializer,
    RegisterSerializer,
    WorkspaceInviteSerializer,
)
from taskite.models import User, Workspace, WorkspaceInvite, WorkspaceMembership
from taskite.exceptions import InvalidInputException
from taskite.tasks import send_verification_email


class ResendEmailThrottle(UserRateThrottle):
    rate = "1/minute"


class AccountsViewSet(ViewSet):

    @action(methods=["GET"], detail=False)
    def status(self, request):
        if request.user.is_authenticated:
            data = {
                "is_authenticated": True,
                "logged_in_user": UserSerializer(request.user).data,
            }
        else:
            data = {"is_authenticated": False, "logged_in_user": None}

        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, url_path="login")
    def login_action(self, request):
        login_serializer = LoginSerializer(data=request.data)
        if not login_serializer.is_valid():
            raise InvalidInputException

        data = login_serializer.validated_data
        user = User.objects.filter(email=data.get("email")).first()
        if not user:
            return Response(
                data={"detail": "No account found with the given email address!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.check_password(data.get("password")):
            return Response(
                data={"detail": "Please enter valid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if user.restricted_at:
            return Response(
                data={
                    "detail": "You'r account has been temporarily blocked. Please contact support for further assistance."
                },
                status=status.HTTP_308_PERMANENT_REDIRECT,
            )

        if user.is_password_expired:
            return Response(
                data={
                    "detail": "Please reset your password to continue using the account."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        login(request, user)
        user_serializer = UserSerializer(user)
        return Response(
            data={"detail": "Login success!", "user": user_serializer.data},
            status=status.HTTP_200_OK,
        )

    @action(methods=["POST"], detail=False)
    def register(self, request):
        register_serializer = RegisterSerializer(data=request.data)
        if not register_serializer.is_valid():
            raise InvalidInputException

        data = register_serializer.validated_data
        existing_user_queryset = User.objects.filter(email=data.get("email"))
        if existing_user_queryset.exists():
            return Response(
                data={
                    "detail": "An account already exists with the given email address."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        password = data.pop("password")
        new_user = User(**data)
        new_user.set_password(password)
        new_user.save()
        send_verification_email.delay(new_user.email)

        login(request, new_user)
        user_serializer = UserSerializer(new_user)
        return Response(
            data={"detail": "Register success!", "user": user_serializer.data},
            status=status.HTTP_200_OK,
        )

    @action(methods=["GET"], detail=False, url_path="logout")
    def logout_action(self, request):
        logout(request)
        return Response(
            data={"detail": "Logout successfull!"}, status=status.HTTP_200_OK
        )

    @action(
        methods=["POST"],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path="resend-verification",
        # throttle_classes=[ResendEmailThrottle],
    )
    def resend_verification(self, request):
        user = request.user
        send_verification_email.delay(user.email)
        return Response(
            data={"detail": "Verification link has been send to your email address."},
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["GET"],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path="pending-invites",
    )
    def pending_invites(self, request):
        workspace_invites = (
            WorkspaceInvite.objects.filter(email=request.user.email, accepted=False)
            .select_related("workspace")
            .select_related("invited_by")
        )
        serializer = WorkspaceInviteSerializer(workspace_invites, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)