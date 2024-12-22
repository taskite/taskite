from rest_framework import serializers

from calyvim.models import Sprint


class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ["id", "name", "start_date", "end_date", "is_active", "created_at"]


class SprintCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=124)
    description = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    is_active = serializers.BooleanField(default=False)
