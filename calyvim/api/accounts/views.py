from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from calyvim.api.accounts.serializers import (
    UserSerializer,
    LoginSerializer,
    RegisterSerializer,
    WorkspaceInviteSerializer,
    UserUpdateSerializer,
    PasswordResetConfirmSerializer,
    PasswordChangeSerializer,
)
from calyvim.models import User, WorkspaceInvite, WorkspaceMembership
from calyvim.exceptions import InvalidInputException
from calyvim.tasks import send_verification_email, send_password_reset_email
from calyvim.throttles import ResendEmailThrottle
from calyvim.utils import update_file_field


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
        invitation_id = data.pop("invitation_id", None)
        if invitation_id:
            # Handle Memberinvites along with register
            invitation = WorkspaceInvite.objects.filter(
                invitation_id=invitation_id
            ).first()
            if not invitation:
                return Response(
                    data={
                        "detail": "No invitation found, seems like invitation has been expired, or deleted."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            data["email"] = invitation.email
        else:
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

        if invitation_id:
            WorkspaceMembership.objects.create(
                workspace=invitation.workspace,
                user=new_user,
                role=WorkspaceMembership.Role.COLLABORATOR,
            )
            invitation.confirm_invitation()
            new_user.verify()
        else:
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
        throttle_classes=[ResendEmailThrottle],
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

    @action(
        methods=["GET", "PATCH"], detail=False, permission_classes=[IsAuthenticated]
    )
    def profile(self, request, *args, **kwargs):
        if request.method == "GET":
            serializer = UserSerializer(request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif request.method == "PATCH":
            update_serializer = UserUpdateSerializer(data=request.data)
            if not update_serializer.is_valid():
                raise InvalidInputException

            data = update_serializer.validated_data

            if "avatar" in data:
                update_file_field(request.user, "avatar", data.get("avatar"))
                del data["avatar"]

            for key, value in data.items():
                setattr(request.user, key, value)

            request.user.save(update_fields=data.keys())
            serializer = UserSerializer(request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"], url_path="password-reset")
    def password_reset(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            return Response(
                data={"detail": "Please enter email address"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(email=email).first()
        if not user:
            return Response(
                data={"detail": "No account found with the given email address."},
                status=status.HTTP_404_NOT_FOUND,
            )

        send_password_reset_email.delay(user.email)
        return Response(
            data={"detail": "Password reset email has been sent to your email address"},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["POST"], url_path="password-reset-confirm")
    def password_reset_confirm(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if not serializer.is_valid():
            raise InvalidInputException

        data = serializer.validated_data
        user = User.objects.filter(
            password_reset_id=data.get("password_reset_id")
        ).first()
        if not user:
            return Response(
                data={"detail": "Invalid password reset token found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.password_reset_confirm(data.get("new_password"))
        login(request, user)

        user_serializer = UserSerializer(user)
        return Response(
            data={
                "detail": "Password reset successfull!",
                "user": user_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["POST"],
        detail=False,
        url_path="password-change",
        permission_classes=[IsAuthenticated],
    )
    def password_change(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data)
        if not serializer.is_valid():
            raise InvalidInputException

        data = serializer.validated_data
        if data.get("new_password") != data.get("confirm_password"):
            return Response(
                data={
                    "detail": "New and confirm password do not match, please enter valid passwords."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not request.user.check_password(data.get("current_password")):
            return Response(
                data={"detail": "Please enter a valid current password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.set_password(data.get("new_password"))
        request.user.save()
        
        return Response(
            data={"detail": "Password changed successfull!"}, status=status.HTTP_200_OK
        )
