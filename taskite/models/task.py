from django.db import models, transaction
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

from taskite.models.base import UUIDTimestampModel


class Task(UUIDTimestampModel):
    class TaskType(models.TextChoices):
        ISSUE = ("issue", "Issue")
        FEATURE = ("feature", "Feature")
        STORY = ("story", "Story")
        BUG = ("bug", "Bug")

    class ActiveTaskManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_archived=False)

    class ArchivedTaskManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_archived=True)

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
    links = ArrayField(base_field=models.TextField(), default=list)
    checklists = ArrayField(base_field=models.JSONField(), default=list)
    estimate = models.ForeignKey(
        "Estimate",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="estimate_tasks",
    )

    # Archived
    is_archived = models.BooleanField(default=False, db_index=True)
    archived_at = models.DateTimeField(blank=True, null=True)

    assignees = models.ManyToManyField(
        "User", through="TaskAssignee", related_name="assigned_tasks"
    )
    labels = models.ManyToManyField(
        "Label", through="TaskLabel", related_name="assigned_label_tasks"
    )

    class Meta:
        db_table = "tasks"
        constraints = [
            models.UniqueConstraint(
                fields=["board", "name"], name="unique_task_name_per_board"
            )
        ]
        ordering = ("sequence",)

    objects = ActiveTaskManager()
    archived_objects = ArchivedTaskManager()
    all_objects = models.Manager()

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

    @transaction.atomic
    def archive(self):
        self.is_archived = True
        self.archived_at = timezone.now()
        self.save(update_fields=["is_archived", "archived_at"])


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


class TaskComment(UUIDTimestampModel):
    class CommentType(models.TextChoices):
        UPDATE = ("update", "Update")
        ACTIVITY = ("activity", "Activity")

    task = models.ForeignKey("Task", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    comment_type = models.CharField(max_length=10, default=CommentType.UPDATE)

    class Meta:
        verbose_name = "Task Comment"
        verbose_name_plural = "Task Comments"
        db_table = "task_comments"

    def __str__(self):
        return str(self.id)


class TaskLabel(UUIDTimestampModel):
    task = models.ForeignKey(
        "Task", on_delete=models.CASCADE, related_name="task_labels"
    )
    label = models.ForeignKey(
        "Label", on_delete=models.CASCADE, related_name="label_task_labels"
    )

    class Meta:
        verbose_name = "Task Label"
        verbose_name_plural = "Task Labels"
        db_table = "task_labels"
        constraints = [
            models.UniqueConstraint(
                fields=["task", "label"], name="unique_label_per_task"
            )
        ]


class TaskAttachment(UUIDTimestampModel):
    task = models.ForeignKey(
        "Task", on_delete=models.CASCADE, related_name="attachments"
    )
    attachment = models.FileField(upload_to="tasks/attachments/")
    filename = models.CharField()
    mime_type = models.CharField(max_length=121)

    class Meta:
        db_table = "task_attachments"

    def __str__(self) -> str:
        return str(self.id)
