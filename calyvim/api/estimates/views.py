from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from calyvim.models import Estimate
from calyvim.mixins import BoardMixin
from calyvim.permissions import BoardGenericPermission
from calyvim.api.estimates.serializers import EstimateSerializer
from calyvim.exceptions import InvalidInputException
from calyvim.utils import get_object_or_raise_api_404


class EstimatesViewSets(BoardMixin, ViewSet):
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
            case "partial_update":
                return [
                    IsAuthenticated(),
                    BoardGenericPermission(allowed_roles=["admin", "maintainer"]),
                ]
            case "destroy":
                return [
                    IsAuthenticated(),
                    BoardGenericPermission(allowed_roles=["admin", "maintainer"]),
                ]
            case _:
                return super().get_permissions()

    def list(self, request, *args, **kwargs):
        estimates = Estimate.objects.filter(board=request.board).order_by("key")
        serializer = EstimateSerializer(estimates, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
