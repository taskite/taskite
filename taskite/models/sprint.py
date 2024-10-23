from django.db import models

from taskite.models.base import UUIDTimestampModel


class Sprint(UUIDTimestampModel):
    class ActiveSprintManager(models.Manager):
        def get_queryset(self) -> models.QuerySet:
            return super().get_queryset().filter(archived_at__isnull=True)

    class ArchiveSprintManager(models.Manager):
        def get_queryset(self) -> models.QuerySet:
            return super().get_queryset().filter(archived_at__isnull=False)

    board = models.ForeignKey("Board", on_delete=models.CASCADE, related_name="sprints")
    name = models.CharField(max_length=124)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()

    archived_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "sprints"
        constraints = [
            models.UniqueConstraint(
                fields=["board", "name"], name="unique_sprint_name_per_board"
            )
        ]

    objects = ActiveSprintManager()
    archive_objects = ArchiveSprintManager()
    all_objects = models.Manager()

    def __str__(self) -> str:
        return self.name
