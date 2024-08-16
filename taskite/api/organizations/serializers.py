from rest_framework import serializers

from taskite.models import Organization, OrganizationUser


class FlatOrganizationUserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='organization.id')
    name = serializers.CharField(source='organization.name')
    boards_count = serializers.IntegerField(source='organization.boards_count')
    created_at = serializers.DateTimeField(source='organization.created_at')
    role = serializers.CharField(source='get_role_display')
    
    class Meta:
        model = OrganizationUser
        fields = [
            "id",
            "name",
            "boards_count",
            "role",
            "created_at",
            "joined_at",
        ]        