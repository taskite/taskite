from rest_framework import serializers

from calyvim.models import Newsline, User


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "display_name",
            "first_name",
            "last_name",
            "avatar",
        ]


class NewslineSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Newsline
        fields = [
            "id",
            "title",
            "status",
            "author",
            "visibility",
            "published_at",
            "created_at",
        ]
