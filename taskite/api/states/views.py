from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from taskite.api.states.serializers import StateSerializer
from taskite.models import State
from taskite.mixins import BoardMixin
from taskite.permissions import BoardCollaboratorPermission, BoardAdminPermission


class StatesViewSet(BoardMixin, ViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'list':
            return [IsAuthenticated(), BoardCollaboratorPermission()]
        elif self.action == 'create':
            return [IsAuthenticated(), BoardAdminPermission()]

        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        states = State.objects.filter(board=request.board).order_by("sequence")
        serializer = StateSerializer(states, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        pass