from django.utils import timezone
from celery import shared_task

from taskite.models import Upload


@shared_task
def confirm_upload(file_path):
    uploaded_file = Upload.objects.filter(key=file_path).first()
    if not uploaded_file:
        uploaded_file = Upload(key=file_path, filename=file_path)

    uploaded_file.confirmed_at = timezone.now()
    uploaded_file.save()


@shared_task
def mark_file_as_deleted(file_path):
    uploaded_file = Upload.objects.filter(key=file_path).first()
    if not uploaded_file:
        pass
        print("No file present")
        return

    uploaded_file.deleted_at = timezone.now()
    uploaded_file.save()
