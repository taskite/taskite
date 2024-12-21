from django.db.models import Q
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from calyvim.utils import get_object_or_raise_api_404
from calyvim.models import Workspace, WorkspaceMembership
from calyvim.api.workspaces.serializers import (
    WorkspaceSerializer,
    WorkspaceMembershipSerializer,
    MemberSerializer,
    WorkspaceCreateSerializer,
    WorkspaceUpdateSerializer,
)
from calyvim.exceptions import WorkspaceNotFoundException, InvalidInputException
from calyvim.utils import update_file_field


class WorkspaceViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        create_serializer = WorkspaceCreateSerializer(data=request.data)
        if not create_serializer.is_valid():
            raise InvalidInputException()

        workspace = Workspace(**create_serializer.validated_data)
        workspace.created_by = request.user
        workspace.save()

        serializer = WorkspaceSerializer(workspace)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        workspaces = Workspace.objects.filter(memberships__user=request.user)
        serializer = WorkspaceSerializer(workspaces, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        workspace = get_object_or_raise_api_404(
            Workspace,
            memberships__user=request.user,
            id=kwargs.get("pk"),
            message="workspace not found.",
        )

        serializer = WorkspaceSerializer(workspace)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        workspace = get_object_or_raise_api_404(
            Workspace,
            memberships__user=request.user,
            id=kwargs.get("pk"),
            message="workspace not found.",
            memberships__role__in=["admin", "maintainer"],
        )

        update_serializer = WorkspaceUpdateSerializer(data=request.data)
        if not update_serializer.is_valid():
            raise InvalidInputException

        data = update_serializer.validated_data

        if "logo" in data:
            update_file_field(workspace, "logo", data.get("logo"))
            del data["logo"]

        for key, value in data.items():
            setattr(workspace, key, value)

        workspace.save(update_fields=data.keys())
        serializer = WorkspaceSerializer(workspace)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=True, url_path="members/search")
    def members_search(self, request, *args, **kwargs):
        workspace = get_object_or_raise_api_404(
            Workspace,
            memberships__user=request.user,
            id=kwargs.get("pk"),
            message="workspace not found.",
        )

        query = request.query_params.get("q")
        if not query:
            return Response(
                data={"detail": "Please enter search query."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        members = workspace.members.filter(
            Q(email__icontains=query)
            | Q(username__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
        ).distinct()
        serializer = MemberSerializer(members, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
