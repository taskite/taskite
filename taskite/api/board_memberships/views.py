from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from taskite.models import BoardMembership
from taskite.permissions import BoardAdminPermission, BoardCollaboratorPermission
from taskite.mixins import BoardMixin
from taskite.api.board_memberships.serializers import (
    BoardMembershipSerializer,
    BoardMembershipCreateSerializer,
    BoardMembershipUpdateSerializer,
)
from taskite.exceptions import (
    InvalidInputException,
    UserNotFoundException,
    TeamNotFoundException,
    BoardMembershipNotFoundException,
)


class BoardMembershipsViewset(BoardMixin, ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        memberships = (
            BoardMembership.objects.filter(board=request.board)
            .select_related("user")
            .select_related("team")
        )
        serializer = BoardMembershipSerializer(memberships, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        MEMBERSHIP_TYPES = ["user", "team"]

        membership_type = request.query_params.get("membership_type")
        if not membership_type or membership_type not in MEMBERSHIP_TYPES:
            return Response(
                data={"detail": "Please provide valid membership type."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        create_serializer = BoardMembershipCreateSerializer(data=request.data)
        if not create_serializer.is_valid():
            raise InvalidInputException

        data = create_serializer.validated_data
        if membership_type == "user":
            user = request.board.workspace.members.filter(
                id=data.get("resource_id")
            ).first()
            if not user:
                raise UserNotFoundException

            queryset = BoardMembership.objects.filter(board=request.board, user=user)
        elif membership_type == "team":
            team = request.board.workspace.teams.filter(
                id=data.get("resource_id")
            ).first()
            if not team:
                raise TeamNotFoundException

            queryset = BoardMembership.objects.filter(board=request.board, team=team)

        if queryset.exists():
            return Response(
                data={"detail": "Membership already exists with the given data."},
                status=status.HTTP_403_FORBIDDEN,
            )

        board_membership = BoardMembership(board=request.board, role=data.get("role"))
        if membership_type == "user":
            board_membership.user = user
        elif membership_type == "team":
            board_membership.team = team

        board_membership.save()
        serializer = BoardMembershipSerializer(board_membership)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        membership = BoardMembership.objects.filter(id=kwargs.get("pk")).first()
        if not membership:
            raise BoardMembershipNotFoundException

        membership.delete()
        return Response(
            data={"detail": "Board membership got deleted."},
            status=status.HTTP_204_NO_CONTENT,
        )

    def partial_update(self, request, *args, **kwargs):
        membership = BoardMembership.objects.filter(id=kwargs.get("pk")).first()
        if not membership:
            raise BoardMembershipNotFoundException

        update_serializer = BoardMembershipUpdateSerializer(data=request.data)
        if not update_serializer.is_valid():
            raise InvalidInputException

        data = update_serializer.validated_data
        for key, value in data.items():
            setattr(membership, key, value)
        membership.save(update_fields=data.keys())
        serializer = BoardMembershipSerializer(membership)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
