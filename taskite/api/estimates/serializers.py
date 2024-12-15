from rest_framework import serializers

from taskite.models import Estimate


class EstimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimate
        fields = [
            "id",
            "key",
            "value",
            "created_at"
        ]
