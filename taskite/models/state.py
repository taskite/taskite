from django.db import models

from taskite.models.base import UUIDTimestampModel


class State(UUIDTimestampModel):
    board = models.ForeignKey("Board", on_delete=models.CASCADE, related_name="states")
    name = models.CharField(max_length=124)
    description = models.TextField(blank=True, null=True)
    sequence = models.FloatField(default=10000)

    class Meta:
        db_table = "states"
        constraints = [
            models.UniqueConstraint(
                fields=["board", "name"], name="unique_state_per_board"
            )
        ]
        ordering = ("sequence",)

    def __str__(self) -> str:
        return f"{self.name}"
