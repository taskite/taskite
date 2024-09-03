import time
from django.contrib.auth import login, logout
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from taskite.api.accounts.serializers import (
    UserSerializer,
    LoginSerializer,
    RegisterSerializer,
)
from taskite.models import User, Workspace, WorkspaceInvite, WorkspaceMembership
from taskite.exceptions import InvalidInputException
from taskite.tasks import verification_email


class AccountsViewSet(ViewSet):

    @action(methods=["GET"], detail=False)
    def status(self, request):
        # time.sleep(1)
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
            print(register_serializer.errors)
            raise InvalidInputException

        data = register_serializer.validated_data
        existing_user = User.objects.filter(email=data.get("email")).first()
        if existing_user:
            return Response(
                data={
                    "detail": "An account already exists with the given email address."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        password = data.pop("password")
        invite_id = request.query_params.get("invite_id", None)
        company = data.pop("company", None)

        if invite_id:
            workspace_invite = WorkspaceInvite.objects.filter(
                id=invite_id, accepted=False
            ).first()
            if not workspace_invite:
                return Response(
                    data={"detail": "Invalid or expired workspace invitation"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                with transaction.atomic():
                    workspace = workspace_invite.workspace
                    new_user = User(**data)
                    new_user.set_password(password)
                    new_user.save()
                    new_user.verify()
                    WorkspaceMembership.objects.create(
                        workspace=workspace,
                        user=new_user,
                        role=WorkspaceMembership.Role.COLLABORATOR,
                    )
                    workspace_invite.accepted = True
                    workspace_invite.save(update_fields=["accepted"])
            except Exception as e:
                print(e)
                return Response(
                    data={"detail": "Failed to create an account"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            try:
                with transaction.atomic():
                    new_user = User(**data)
                    new_user.set_password(password)
                    new_user.save()
                    if not company:
                        company = f"{new_user.first_name}'s space"
                    workspace = Workspace(name=company, created_by=new_user)
                    workspace.save()
                    verification_email.delay(new_user.email)
            except Exception as e:
                print(e)
                return Response(
                    data={"detail": "Failed to create an account"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

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
    )
    def resend_verification(self, request):
        user = request.user
        verification_email.delay(user.email)
        return Response(
            data={"detail": "Verification link has been send to your email address."},
            status=status.HTTP_200_OK,
        )
