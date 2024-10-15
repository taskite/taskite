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
    cover = models.ImageField(blank=True, null=True, upload_to="attachments/")
    task_number_counter = models.IntegerField(default=1)
    task_prefix = models.CharField(max_length=5, blank=True)
    tasks_count = models.IntegerField(default=0)
    members_count = models.IntegerField(default=0)

    archived_at = models.DateTimeField(blank=True, null=True)

    users = models.ManyToManyField(
        "User",
        through="BoardPermission",
        related_name="boards",
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


class BoardTeamPermission(UUIDTimestampModel):
    ROLE_CHOICES = [("admin", "Admin"), ("collaborator", "Collaborator")]

    board = models.ForeignKey(
        "Board", on_delete=models.CASCADE, related_name="team_memberships"
    )
    team = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="team_board_team_memberships"
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="collaborator")

    class Meta:
        db_table = "board_team_permissions"

    def __str__(self) -> str:
        return str(self.id)


class BoardPermission(UUIDTimestampModel):
    class UserBoardPermissionManager(models.Manager):
        def get_queryset(self):
            return (
                super()
                .get_queryset()
                .filter(team_permission__isnull=True, team_membership__isnull=True)
                .filter(workspace_membership__isnull=False)
            )

    class TeamBoardPermissionManager(models.Manager):
        def get_queryset(self):
            return (
                super()
                .get_queryset()
                .filter(workspace_membership__isnull=True)
                .filter(team_permission__isnull=False, team_membership__isnull=False)
            )

    ROLE_CHOICES = [("admin", "Admin"), ("collaborator", "Collaborator")]

    board = models.ForeignKey(
        "Board", on_delete=models.CASCADE, related_name="permissions"
    )
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_board_permissions"
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="collaborator")
    team_permission = models.ForeignKey(
        "BoardTeamPermission",
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
        db_table = "board_permissions"

    objects = models.Manager()
    user_objects = UserBoardPermissionManager()
    team_objects = TeamBoardPermissionManager()

    def __str__(self):
        return str(self.id)
