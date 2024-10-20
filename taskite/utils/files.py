from django.core.files.storage import default_storage
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from taskite.tasks import file_promote, file_archive


def update_file_field(instance, key, new_file_name):
    old_file = getattr(instance, key, None)

    if old_file:
        # File already present
        if old_file.name != new_file_name:
            setattr(instance, key, new_file_name)
            instance.save(update_fields=[key])

            if new_file_name is not None:
                file_promote.delay(new_file_name)
            file_archive.delay(old_file.name)
    else:
        # No file is present
        if new_file_name:
            setattr(instance, key, new_file_name)
            instance.save(update_fields=[key])

            file_promote.delay(new_file_name)


def s3_file_copy_helper(source_path, destination_path):
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


def s3_file_move_helper(source_path, destination_path):
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

        print(f"File successfully moved from {source_path} to {destination_path} in S3")
    except ClientError as e:
        print(f"Error moving file in S3: {str(e)}")


def local_file_copy_helper(source_path, destination_path):
    print('Source Path', source_path)
    print('Destination Path', destination_path)

    try:
        if default_storage.exists(source_path):
            file_content = default_storage.open(source_path).read()
            default_storage.save(destination_path, file_content)
            print(
                f"File successfully copied from {source_path} to {destination_path} locally"
            )
        else:
            print(f"Source file {source_path} does not exist")
    except Exception as e:
        print(f"Error copying file locally: {str(e)}")


def local_file_move_helper(source_path, destination_path):
    try:
        if default_storage.exists(source_path):
            file_content = default_storage.open(source_path).read()
            default_storage.save(destination_path, file_content)
            default_storage.delete(source_path)
            print(
                f"File successfully moved from {source_path} to {destination_path} locally"
            )
        else:
            print(f"Source file {source_path} does not exist")
    except Exception as e:
        print(f"Error moving file locally: {str(e)}")
