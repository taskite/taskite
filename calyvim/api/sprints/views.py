from django.db import transaction
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from calyvim.models import Sprint
from calyvim.mixins import BoardMixin
from calyvim.api.sprints.serializers import SprintSerializer, SprintCreateSerializer
from calyvim.permissions import BoardGenericPermission
from calyvim.exceptions import InvalidInputException


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

    def create(self, request, *args, **kwargs):
        create_serializer = SprintCreateSerializer(data=request.data)
        if not create_serializer.is_valid():
            raise InvalidInputException

        data = create_serializer.validated_data
        with transaction.atomic():
            if data.get("is_active"):
                Sprint.objects.filter(board=request.board, is_active=True).update(
                    is_active=False
                )

            sprint = Sprint.objects.create(
                board=request.board,
                **data,
            )

        serializer = SprintSerializer(sprint)
        response_data = {
            "detail": f"The sprint '{sprint.name}' has been created successfully.",
            "sprint": serializer.data,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        sprints = Sprint.objects.filter(board=request.board).order_by("-created_at")
        serializer = SprintSerializer(sprints, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
