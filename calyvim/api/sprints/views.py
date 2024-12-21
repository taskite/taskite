from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from calyvim.models import Sprint
from calyvim.mixins import BoardMixin
from calyvim.api.sprints.serializers import SprintSerializer
from calyvim.permissions import BoardGenericPermission


class SprintsViewSet(BoardMixin, ViewSet):
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
        sprints = Sprint.objects.filter(board=request.board).order_by("-created_at")
        serializer = SprintSerializer(sprints, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)