import uuid
from django.db import models


class State(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    board = models.ForeignKey("Board", on_delete=models.CASCADE, related_name="states")
    name = models.CharField(max_length=124)
    description = models.TextField(blank=True, null=True)
    sequence = models.FloatField(default=10000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "states"
        constraints = [
            models.UniqueConstraint(fields=["board", "name"], name="unique_state_per_board")
        ]
        ordering = ("sequence",)