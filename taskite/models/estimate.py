from django.db import models

from taskite.models.base import UUIDTimestampModel


class Estimate(UUIDTimestampModel):
    board = models.ForeignKey(
        "Board", on_delete=models.CASCADE, related_name="estimates"
    )
    key = models.IntegerField(default=1)
    description = models.TextField(blank=True, null=True)
    value = models.CharField(max_length=30)

    class Meta:
        db_table = "estimates"

    def __str__(self):
        return str(self.id)
