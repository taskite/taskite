from django.db import models

from taskite.models.base import UUIDTimestampModel


class Sprint(UUIDTimestampModel):
    board = models.ForeignKey("Board", on_delete=models.CASCADE, related_name="sprints")
    name = models.CharField(max_length=124)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = "sprints"

    def __str__(self) -> str:
        return self.name
