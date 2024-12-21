from rest_framework import serializers

from calyvim.models import Sprint


class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ["id", "name", "start_date", "end_date", "is_active", "created_at"]
