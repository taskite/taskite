from rest_framework import serializers


class PreSignedSerializer(serializers.Serializer):
    file_name = serializers.CharField()
    file_type = serializers.CharField()
    model_name = serializers.CharField()
    model_field = serializers.CharField()
