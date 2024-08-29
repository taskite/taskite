from rest_framework import serializers

from taskite.models.priority import Priority


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = [
            "id",
            "board_id",
            "name",
            "created_at"
        ]