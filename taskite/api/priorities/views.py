from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from taskite.models.priority import Priority
from taskite.permissions import BoardPermission
from taskite.mixins import BoardMixin
from taskite.api.priorities.serializers import PrioritySerializer


class PrioritiesViewSet(BoardMixin, ViewSet):
    permission_classes = [IsAuthenticated, BoardPermission]

    def list(self, request, *args, **kwargs):
        priorities = Priority.objects.filter(board=request.board)
        serializer = PrioritySerializer(priorities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)