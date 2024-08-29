from django.db import models

from taskite.models.base import UUIDTimestampModel


class Task(UUIDTimestampModel):
    class TaskType(models.TextChoices):
        ISSUE = ("issue", "Issue")
        FEATURE = ("feature", "Feature")
        STORY = ("story", "Story")
        BUG = ("bug", "Bug")

    board = models.ForeignKey(
        "Board", on_delete=models.CASCADE, related_name="board_tasks"
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="subtasks", blank=True, null=True
    )
    state = models.ForeignKey(
        "State", on_delete=models.SET_NULL, related_name="tasks", null=True
    )
    priority = models.ForeignKey(
        "Priority", on_delete=models.SET_NULL, null=True, related_name="priority_tasks"
    )
    sprint = models.ForeignKey(
        "Sprint",
        on_delete=models.SET_NULL,
        null=True,
        related_name="sprint_tasks",
        blank=True,
    )
    task_type = models.CharField(
        max_length=10, choices=TaskType.choices, default=TaskType.ISSUE
    )
    created_by = models.ForeignKey(
        "User", on_delete=models.SET_NULL, null=True, related_name="created_tasks"
    )
    number = models.IntegerField(blank=True, editable=False)
    name = models.CharField(max_length=10, blank=True, editable=False)
    summary = models.CharField(max_length=225)
    description = models.TextField(blank=True, null=True)
    sequence = models.FloatField(default=50000, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    archived_at = models.DateTimeField(blank=True, null=True)

    assignees = models.ManyToManyField(
        "User", through="TaskAssignee", related_name="assigned_tasks"
    )

    class Meta:
        db_table = "tasks"
        constraints = [
            models.UniqueConstraint(
                fields=["board", "name"], name="unique_task_name_per_board"
            )
        ]
        ordering = ("sequence",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding:
            board = self.board
            state = self.state

            # Get the last task sequence in the state
            last_task_in_state = (
                Task.objects.filter(board=board, state=state)
                .order_by("-sequence")
                .first()
            )
            if last_task_in_state is not None:
                self.sequence = last_task_in_state.sequence + 10000

            self.number = board.task_number_counter
            self.name = f"{board.task_prefix}-{board.task_number_counter}"

            board.task_number_counter += 1
            board.tasks_count += 1
            board.save(
                update_fields=["task_number_counter", "task_prefix", "tasks_count"]
            )
        return super().save(*args, **kwargs)


class TaskAssignee(UUIDTimestampModel):
    task = models.ForeignKey(
        "Task", on_delete=models.CASCADE, related_name="task_assignees"
    )
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_task_assignees"
    )

    class Meta:
        verbose_name = "Task Assignee"
        verbose_name_plural = "Task Assignees"
        db_table = "task_assignees"
        constraints = [
            models.UniqueConstraint(
                fields=["task", "user"], name="unique_assignee_per_task"
            )
        ]

    def __str__(self) -> str:
        return str(self.id)
