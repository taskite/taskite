from django.db import models

from taskite.models.base import UUIDModel


class PurgedAsset(UUIDModel):
    bucket = models.CharField(max_length=124, default="local")
    key = models.CharField(max_length=225)
    purged_at = models.DateTimeField()

    class Meta:
        db_table = "purged_assets"

    def __str__(self) -> str:
        return self.key


class UnusedAsset(UUIDModel):
    bucket = models.CharField(max_length=124, default="local")
    key = models.CharField(max_length=225, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "unused_assets"

    def __str__(self) -> str:
        return self.key
