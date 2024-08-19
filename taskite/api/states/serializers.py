from rest_framework import serializers

from taskite.models import State


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = [
            "id",
            "name",
            "description",
            "sequence",
            "created_at"
        ]