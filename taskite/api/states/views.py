from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from taskite.api.states.serializers import StateSerializer
from taskite.models import State
from taskite.mixins import BoardMixin
from taskite.permissions import BoardViewPermission


class StatesViewSet(BoardMixin, ViewSet):
    permission_classes = [IsAuthenticated, BoardViewPermission]

    def list(self, request, *args, **kwargs):
        states = State.objects.filter(board=request.board).order_by("sequence")
        serializer = StateSerializer(states, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)