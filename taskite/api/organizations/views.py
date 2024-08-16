from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status

from taskite.models import Organization, OrganizationUser
from taskite.api.organizations.serializers import FlatOrganizationUserSerializer


class OrganizationViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        organization_users = OrganizationUser.objects.filter(
            user=request.user
        ).select_related("organization")
        serializer = FlatOrganizationUserSerializer(organization_users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
