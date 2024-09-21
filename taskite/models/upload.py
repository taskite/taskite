from django.db import models

from taskite.models.base import UUIDTimestampModel


class Upload(UUIDTimestampModel):
    key = models.CharField(max_length=225, unique=True)
    filename = models.CharField(max_length=124)
    associated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "uploads"

    def __str__(self) -> str:
        return self.key