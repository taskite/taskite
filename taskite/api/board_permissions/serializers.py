from rest_framework import serializers

from taskite.models import BoardPermission, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "avatar"]


class BoardPermissionSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = BoardPermission
        fields = ["id", "user", "role", "created_at"]


class BoardPermissionCreateSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    role = serializers.CharField()


class BoardPermissionUpdateSerializer(serializers.Serializer):
    role = serializers.CharField()