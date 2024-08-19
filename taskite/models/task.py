import uuid
from django.db import models


class Task(models.Model):
    class TaskType(models.TextChoices):
        ISSUE = ("issue", "Issue")
        FEATURE = ("feature", "Feature")
        STORY = ("story", "Story")
        BUG = ("bug", "Bug")

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    board = models.ForeignKey(
        "Board", on_delete=models.CASCADE, related_name="board_tasks"
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="subtasks"
    )
    state = models.ForeignKey(
        "State", on_delete=models.SET_NULL, related_name="tasks", null=True
    )
    priority = models.ForeignKey(
        "Priority", on_delete=models.SET_NULL, null=True, related_name="priority_tasks"
    )
    task_type = models.CharField(
        max_length=10, choices=TaskType.choices, default=TaskType.ISSUE
    )
    created_by = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)
    number = models.IntegerField(blank=True)
    name = models.CharField(max_length=10, blank=True)
    summary = models.CharField(max_length=225)
    description = models.TextField(blank=True, null=True)
    sequence = models.FloatField(default=50000)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    archived_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "tasks"
        constraints = [
            models.UniqueConstraint(
                fields=["board", "name"], name="unique_task_name_per_board"
            )
        ]
        ordering = ("sequence",)
