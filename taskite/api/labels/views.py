from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from taskite.models import Label
from taskite.mixins import BoardMixin
from taskite.api.labels.serializers import LabelSerializer


class LabelsViewSet(BoardMixin, ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        labels = Label.objects.filter(board=request.board).order_by("name")
        serializer = LabelSerializer(labels, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
