from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from calyvim.models.priority import Priority
from calyvim.mixins import BoardMixin
from calyvim.api.priorities.serializers import PrioritySerializer
from calyvim.permissions import BoardGenericPermission


class PrioritiesViewSet(BoardMixin, ViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        match self.action:
            case "list":
                return [IsAuthenticated(), BoardGenericPermission()]
            case "create":
                return [
                    IsAuthenticated(),
                    BoardGenericPermission(allowed_roles=["admin", "maintainer"]),
                ]
            case _:
                return super().get_permissions()

    def list(self, request, *args, **kwargs):
        priorities = Priority.objects.filter(board=request.board)
        serializer = PrioritySerializer(priorities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)