from django.db import models

from taskite.models.base import UUIDTimestampModel


class Upload(UUIDTimestampModel):
    bucket = models.CharField(max_length=124, blank=True, null=True)
    key = models.CharField(max_length=225, unique=True)
    filename = models.CharField(max_length=124)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    # Audit fields
    uploaded_by_email = models.EmailField(blank=True, null=True)

    class Meta:
        db_table = "uploads"

    def __str__(self) -> str:
        return self.key