from django.db import models

from taskite.models.base import UUIDTimestampModel


class Priority(UUIDTimestampModel):
    board = models.ForeignKey(
        "Board", on_delete=models.CASCADE, related_name="priorities"
    )
    name = models.CharField(max_length=124)

    class Meta:
        verbose_name = "Priority"
        verbose_name_plural = "Priorities"
        db_table = "priorities"
        constraints = [
            models.UniqueConstraint(
                fields=["board", "name"], name="unique_priority_per_board"
            )
        ]
        ordering = ("created_at",)

    def __str__(self) -> str:
        return f"{self.name}"
