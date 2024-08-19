import uuid
from django.db import models


class Priority(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    board = models.ForeignKey(
        "Board", on_delete=models.CASCADE, related_name="priorities"
    )
    name = models.CharField(max_length=124)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
