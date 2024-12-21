from django.db.models import Q
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from calyvim.utils import get_object_or_raise_api_404
from calyvim.exceptions import InvalidInputException
from calyvim.models import Workspace, WorkspaceMembership, Newsline
from calyvim.api.newslines.serializers import NewslineSerializer


class NewslinesViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def get_workspace_membership(self, user, workspace):
        workspace_membership = get_object_or_raise_api_404(
            WorkspaceMembership, user=user, workspace=workspace
        )
        return workspace_membership

    def list(self, request, *args, **kwargs):
        workspace_id = request.query_params.get("workspace_id")
        if not workspace_id:
            raise InvalidInputException

        workspace = get_object_or_raise_api_404(Workspace, id=workspace_id)
        workspace_membership = self.get_workspace_membership(
            request.user, workspace=workspace
        )

        if workspace_membership.Role == WorkspaceMembership.Role.ADMIN:
            newslines = Newsline.published_objects.filter(workspace=workspace)
        else:
            newslines = Newsline.published_objects.filter(
                Q(visibility=Newsline.Visibility.PUBLIC)
                | Q(permissions__user=request.user)
            ).distinct()

        newslines = newslines.select_related("author")
        serializer = NewslineSerializer(newslines, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
