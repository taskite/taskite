from django.db import models
from django.utils.text import slugify

from taskite.models.base import UUIDTimestampModel


class Board(UUIDTimestampModel):
    workspace = models.ForeignKey(
        "Workspace", on_delete=models.CASCADE, related_name="boards"
    )
    name = models.CharField(max_length=124)
    slug = models.SlugField(max_length=124, blank=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        "User", on_delete=models.SET_NULL, null=True, related_name="created_boards"
    )
    cover = models.ImageField(blank=True, null=True, upload_to="boards/covers/")
    task_number_counter = models.IntegerField(default=1)
    task_prefix = models.CharField(max_length=5, blank=True)
    tasks_count = models.IntegerField(default=0)
    members_count = models.IntegerField(default=0)

    archived_at = models.DateTimeField(blank=True, null=True)

    users = models.ManyToManyField(
        "User",
        through="BoardMembership",
        related_name="boards",
    )
    teams = models.ManyToManyField(
        "Team", through="BoardMembership", related_name="boards"
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "boards"
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "slug"], name="unqiue_board_slug_per_workspace"
            )
        ]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.slug:
                self.slug = slugify(self.name)
                
            # Generate task prefix if not given
            if not self.task_prefix:
                self.task_prefix = self.generate_acronym(self.name)
        return super().save(*args, **kwargs)

    def generate_acronym(self, name):
        words = name.split()

        # Case for a single word
        if len(words) == 1:
            return words[0][0].upper() + words[0][-1].upper()

        # Case for two or more words
        else:
            return "".join(word[0].upper() for word in words[:2])


class BoardMembership(UUIDTimestampModel):
    class Role(models.TextChoices):
        ADMIN = ("admin", "Admin")
        COLLABORATOR = ("collaborator", "Collaborator")

    board = models.ForeignKey(
        "Board", on_delete=models.CASCADE, related_name="memberships"
    )
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="board_memberships",
        blank=True,
        null=True,
    )
    team = models.ForeignKey(
        "Team",
        on_delete=models.CASCADE,
        related_name="team_board_memberships",
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.COLLABORATOR
    )

    class Meta:
        db_table = "board_memberships"
        constraints = [
            # models.UniqueConstraint(
            #     fields=["board", "user"], name="unique_member_per_board"
            # )
        ]

    def __str__(self) -> str:
        return str(self.id)
