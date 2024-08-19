from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from taskite.models import Board, Organization, OrganizationUser
from taskite.api.boards.serializers import BoardSerializer, BoardCreateSerializer
from taskite.exceptions import InvalidInputException, OrganizationNotFoundException


class BoardsViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        organizations = Organization.objects.filter(users__user=request.user)
        boards = Board.objects.filter(organization__in=organizations).select_related(
            "created_by"
        )
        serializer = BoardSerializer(boards, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        create_serializer = BoardCreateSerializer(data=request.data)
        if not create_serializer.is_valid():
            raise InvalidInputException

        data = create_serializer.validated_data

        # Check for org permission
        organization_id = data.pop("organization_id")
        organization_user = OrganizationUser.objects.filter(
            organization__id=organization_id,
            user=request.user,
            role__in=[OrganizationUser.Role.OWNER, OrganizationUser.Role.ADMIN],
        ).first()
        if not organization_user:
            raise OrganizationNotFoundException

        try:
            board = Board(
                **data,
                created_by=request.user,
                organization=organization_user.organization
            )
            board.save()
        except Exception as e:
            print(e)
            return Response(
                data={"detail": "Failed to create board."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        board_serializer = BoardSerializer(board)
        return Response(data=board_serializer.data, status=status.HTTP_201_CREATED)
