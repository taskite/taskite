from typing import Iterable
from django.db import models

from calyvim.models.base import UUIDTimestampModel


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

    def save(self, *args, **kwargs):
        if self._state.adding:
            # last state
            last_state = (
                State.objects.filter(board=self.board).order_by("-sequence").first()
            )
            if last_state:
                self.sequence = last_state.sequence + 10000
        return super().save(*args, **kwargs)
