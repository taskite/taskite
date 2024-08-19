from rest_framework import serializers

from taskite.models import Board, User


class BoardCreateSerializer(serializers.Serializer):
    organization_id = serializers.UUIDField()
    name = serializers.CharField()
    visibility = serializers.ChoiceField(choices=Board.Visibility.choices)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class CreatedBySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
        ]


class BoardSerializer(serializers.ModelSerializer):
    created_by = CreatedBySerializer()

    class Meta:
        model = Board
        fields = [
            "id",
            "name",
            "organization_id",
            "created_by",
            "description",
            "task_prefix",
            "visibility",
            "created_at",
        ]
