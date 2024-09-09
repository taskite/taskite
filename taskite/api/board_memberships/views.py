from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from taskite.models import BoardMembership
from taskite.permissions import BoardAdminPermission, BoardCollaboratorPermission
from taskite.mixins import BoardMixin
from taskite.api.board_memberships.serializers import BoardMembershipSerializer


class BoardMembershipsViewset(BoardMixin, ViewSet):
    permission_classes = []

    def list(self, request, *args, **kwargs):
        memberships = (
            BoardMembership.objects.filter(board=request.board)
            .select_related("user")
            .select_related("team")
        )
        serializer = BoardMembershipSerializer(memberships, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
