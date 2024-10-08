from django.db import models

from taskite.models.base import UUIDTimestampModel


class Label(UUIDTimestampModel):
    board = models.ForeignKey("Board", on_delete=models.CASCADE, related_name="labels")
    name = models.CharField(max_length=124)
    color = models.CharField(max_length=10)

    class Meta:
        db_table = "labels"
        constraints = [
            models.UniqueConstraint(
                fields=["board", "name"], name="unqiue_label_name_per_board"
            )
        ]

    def __str__(self) -> str:
        return self.name
