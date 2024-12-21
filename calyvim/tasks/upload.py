import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from celery import shared_task
import boto3
from botocore.exceptions import ClientError
from django.conf import settings

@shared_task
def file_promote(file_key):
    if settings.USE_S3:
        source_path = os.path.join("cache", file_key)
        destination_path = os.path.join("uploads", file_key)
        s3 = boto3.client("s3")
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        try:
            # Copy the file to the new location
            s3.copy_object(
                Bucket=bucket_name,
                CopySource={"Bucket": bucket_name, "Key": source_path},
                Key=destination_path,
            )

            print(
                f"File successfully copied from {source_path} to {destination_path} in S3"
            )
        except ClientError as e:
            print(f"Error copying file in S3: {str(e)}")
    else:
        cache_storage = FileSystemStorage(location=settings.CACHE_MEDIA_ROOT)
        if not cache_storage.exists(file_key):
            print(f"Source file does not exist")
        file_content = cache_storage.open(file_key)
        default_storage.save(file_key, file_content)


@shared_task
def file_archive(file_key):
    if settings.USE_S3:
        source_path = os.path.join("uploads", file_key)
        destination_path = os.path.join("archive", file_key)
        s3 = boto3.client("s3")
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        try:
            # Copy the file to the new location
            s3.copy_object(
                Bucket=bucket_name,
                CopySource={"Bucket": bucket_name, "Key": source_path},
                Key=destination_path,
            )

            # Delete the original file
            s3.delete_object(Bucket=bucket_name, Key=source_path)

            print(
                f"File successfully moved from {source_path} to {destination_path} in S3"
            )
        except ClientError as e:
            print(f"Error moving file in S3: {str(e)}")
    else:
        archive_storage = FileSystemStorage(location=settings.ARCHIVE_MEDIA_ROOT)
        if not default_storage.exists(file_key):
            print(f"Source file does not exist")

        file_content = default_storage.open(file_key)
        archive_storage.save(file_key, file_content)

        default_storage.delete(file_key)
