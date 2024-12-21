from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from calyvim.models import State
from calyvim.mixins import BoardMixin
from calyvim.permissions import BoardGenericPermission
from calyvim.api.states.serializers import (
    StateSequenceUpdateSerializer,
    StateUpdateSerializer,
    StateSerializer,
    StateCreateSerializer,
)
from calyvim.exceptions import InvalidInputException
from calyvim.utils import get_object_or_raise_api_404


class StatesViewSet(BoardMixin, ViewSet):
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
                    BoardGenericPermission(allowed_roles=["admin", "maintainer"])
                ]
            case "destroy":
                return [
                    IsAuthenticated(),
                    BoardGenericPermission(allowed_roles=["admin", "maintainer"]),
                ]
            case "update_sequence":
                return [
                    IsAuthenticated(),
                    BoardGenericPermission(
                        allowed_roles=["admin", "maintainer", "collaborator"]
                    ),
                ]
            case _:
                return super().get_permissions()

    def list(self, request, *args, **kwargs):
        states = State.objects.filter(board=request.board).order_by("sequence")
        serializer = StateSerializer(states, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        create_serializer = StateCreateSerializer(data=request.data)
        if not create_serializer.is_valid():
            raise InvalidInputException

        data = create_serializer.validated_data
        state = State.objects.create(board=request.board, **data)

        serializer = StateSerializer(state)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        state = get_object_or_raise_api_404(
            State, board=request.board, id=kwargs.get("pk")
        )
        update_serializer = StateUpdateSerializer(data=request.data)
        if not update_serializer.is_valid():
            raise InvalidInputException

        data = update_serializer.validated_data
        for key, value in data.items():
            setattr(state, key, value)
        state.save(update_fields=data.keys)

        serializer = StateSerializer(state)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        state = get_object_or_raise_api_404(
            State, board=request.board, id=kwargs.get("pk")
        )
        state.delete()
        return Response(
            data={"detail": "State got deleted."}, status=status.HTTP_204_NO_CONTENT
        )

    @action(methods=["PATCH"], detail=True, url_path="update-sequence")
    def update_sequence(self, request, *args, **kwargs):
        serializer = StateSequenceUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            raise InvalidInputException

        state = get_object_or_raise_api_404(
            State, board=request.board, id=kwargs.get("pk")
        )

        data = serializer.validated_data
        if data.get("previous_state") and data.get("next_state"):
            previous_state = get_object_or_raise_api_404(
                State, board=request.board, id=data.get("previous_state")
            )
            next_state = get_object_or_raise_api_404(
                State, board=request.board, id=data.get("next_state")
            )
            state.sequence = (previous_state.sequence + next_state.sequence) / 2

        elif data.get("previous_state"):
            previous_state = get_object_or_raise_api_404(
                State, board=request.board, id=data.get("previous_state")
            )
            state.sequence = previous_state.sequence + 10000

        elif data.get("next_state"):
            next_state = get_object_or_raise_api_404(
                State, board=request.board, id=data.get("next_state")
            )
            state.sequence = next_state.sequence / 2

        state.save(update_fields=["sequence"])
        return Response(
            data={"detail": "State sequence updated", "new_sequence": state.sequence},
            status=status.HTTP_200_OK,
        )
