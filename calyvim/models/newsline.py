from django.db import models

from calyvim.models.base import UUIDTimestampModel


class Newsline(UUIDTimestampModel):
    class PublishedNewslineManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status=Newsline.Status.PUBLISHED)

    class Status(models.TextChoices):
        PUBLISHED = ("published", "Published")
        DRAFT = ("draft", "Draft")
        ARCHIVED = ("archived", "Archived")

    class Visibility(models.TextChoices):
        PUBLIC = ("public", "Public")
        RESTRICTED = ("restricted", "Restricted")

    workspace = models.ForeignKey(
        "Workspace", on_delete=models.CASCADE, related_name="newslines"
    )
    title = models.CharField(max_length=512)
    content = models.TextField()
    author = models.ForeignKey(
        "User", on_delete=models.SET_NULL, null=True, related_name="author_newslines"
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT
    )
    visibility = models.CharField(
        max_length=20, choices=Visibility.choices, default=Visibility.PUBLIC
    )
    allow_comment = models.BooleanField(default=True)

    published_at = models.DateTimeField(blank=True, null=True)
    archived_at = models.DateTimeField(blank=True, null=True)

    published_objects = PublishedNewslineManager()
    objects = models.Manager()

    class Meta:
        db_table = "newslines"

    def __str__(self):
        return self.title


class NewslineTeamPermission(UUIDTimestampModel):
    newsline = models.ForeignKey(
        "Newsline", on_delete=models.CASCADE, related_name="team_permissions"
    )
    team = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="team_newsline_team_permissions"
    )

    class Meta:
        db_table = "newsline_team_permissions"

    def __str__(self):
        return str(self.id)


class NewslinePermission(UUIDTimestampModel):
    newsline = models.ForeignKey(
        "Newsline", on_delete=models.CASCADE, related_name="permissions"
    )
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_newsline_permissions"
    )
    team_permission = models.ForeignKey(
        "NewslineTeamPermission",
        related_name="+",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    workspace_membership = models.ForeignKey(
        "WorkspaceMembership",
        related_name="+",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    team_membership = models.ForeignKey(
        "TeamMembership",
        related_name="+",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "newsline_permissions"

    def __str__(self):
        return str(self.id)


class NewslineComment(UUIDTimestampModel):
    newsline = models.ForeignKey(
        "Newsline", on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_newsline_comments"
    )
    content = models.TextField()

    class Meta:
        db_table = "newsline_comments"

    def __str__(self):
        return str(self.id)


class NewslineRead(UUIDTimestampModel):
    newsline = models.ForeignKey(
        "Newsline", on_delete=models.CASCADE, related_name="reads"
    )
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_newsline_reads"
    )

    class Meta:
        db_table = "newsline_reads"
        constraints = [
            models.UniqueConstraint(
                fields=["newsline", "user"], name="unique_newsline_user_read"
            )
        ]

    def __str__(self):
        return str(self.id)
