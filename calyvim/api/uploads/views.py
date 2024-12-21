from django.conf import settings
import os
from botocore.exceptions import ClientError
import boto3
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.apps import apps
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status

from calyvim.api.uploads.serializers import PreSignedSerializer
from calyvim.exceptions import InvalidInputException


class UploadsViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def get_model_field_upload_path(self, model_name, model_field):
        model = apps.get_model("calyvim", model_name)
        field = model._meta.get_field(model_field)
        return field.upload_to

    def generate_unique_file_key(self, model_name, model_field, original_filename):
        self.get_model_field_upload_path(model_name, model_field)

        # Get the file extension
        _, file_extension = os.path.splitext(original_filename)

        # Generate a timestamp string
        timestamp = timezone.now().strftime("%Y%m%d")

        # Combine all parts to create a unique filename
        unique_filename = (
            f"{timestamp}_{get_random_string(8)}_{get_random_string(8)}{file_extension}"
        )

        # path prefix
        path_prefix = self.get_model_field_upload_path(model_name, model_field)

        # Prepend the base 'uploads' folder
        file_key = os.path.join(path_prefix, unique_filename)

        return file_key

    def generate_s3_presigned_url(self, file_key):
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )
        try:
            url = s3_client.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
                    "Key": "cache/" + file_key,
                },
                ExpiresIn=3600,  # URL expires in 1 hour
            )
            return url
        except ClientError as e:
            print(f"Error generating pre-signed URL: {e}")
            return None

    def get_file_src(self, file_key):
        return f"https://s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{settings.AWS_STORAGE_BUCKET_NAME}/cache/{file_key}"

    def get_local_file_upload_url(self, file_key):
        return f"http://localhost:8000/upload/{file_key}"

    def get_local_file_src(self, file_key):
        return f"http://localhost:8000{settings.MEDIA_URL}cache/{file_key}"

    @action(methods=["POST"], detail=False, url_path="presigned-url")
    def presigned_url(self, request):
        serializer = PreSignedSerializer(data=request.data)
        if not serializer.is_valid():
            return InvalidInputException

        data = serializer.validated_data

        file_key = self.generate_unique_file_key(
            data.get("model_name"), data.get("model_field"), data.get("file_name")
        )

        if settings.USE_S3:
            data = {
                "file_key": file_key,
                "file_upload_url": self.generate_s3_presigned_url(file_key),
                "file_src": self.get_file_src(file_key),
            }

        else:
            data = {
                "file_key": file_key,
                "file_upload_url": self.get_local_file_upload_url(file_key),
                "file_src": self.get_local_file_src(file_key),
            }
        return Response(data, status=status.HTTP_200_OK)
