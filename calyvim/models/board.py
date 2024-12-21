from django.db import models, IntegrityError

# from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.apps import apps

from calyvim.models.base import UUIDTimestampModel
from calyvim.models.choice import BoardPermissionRole


class Board(UUIDTimestampModel):
    class TemplateBoardManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_template=True)

    class EstimateType(models.TextChoices):
        POINT = ("point", "Point")
        CATEGORY = ("category", "Category")
        TIME = ("time", "Time")

    workspace = models.ForeignKey(
        "Workspace", on_delete=models.CASCADE, related_name="boards"
    )
    name = models.CharField(max_length=124)
    slug = models.SlugField(max_length=124, blank=True, unique=True, editable=False)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        "User", on_delete=models.SET_NULL, null=True, related_name="created_boards"
    )
    logo = models.ImageField(blank=True, null=True, upload_to="boards/logos/")
    cover = models.ImageField(blank=True, null=True, upload_to="boards/covers/")
    task_number_counter = models.IntegerField(default=1)
    task_prefix = models.CharField(max_length=5, blank=True)
    tasks_count = models.IntegerField(default=0)
    members_count = models.IntegerField(default=0)
    is_estimate_enabled = models.BooleanField(default=False)
    estimate_type = models.CharField(
        max_length=10, choices=EstimateType.choices, default=EstimateType.TIME
    )
    archived_at = models.DateTimeField(blank=True, null=True)

    # Template Related Settings
    is_template = models.BooleanField(
        default=False,
        help_text="WARN: Enabling this would make board public for other people to copy as template",
    )
    template = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="copies",
        help_text="If this board was created from a template, reference to the template board",
    )
    is_from_template = models.BooleanField(
        default=False, help_text="Indicates if this board was created from a template"
    )

    users = models.ManyToManyField(
        "User",
        through="BoardPermission",
        related_name="boards",
    )

    objects = models.Manager()
    template_objects = TemplateBoardManager()

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "boards"

    def __str__(self) -> str:
        return self.name

    def generate_project_slug(self):
        """Handles retry mechanism to generate a unique slug."""
        max_attempts = 3
        for _ in range(max_attempts):
            slug = get_random_string(16)
            if not self.__class__.objects.filter(slug=slug).exists():
                return slug
        raise IntegrityError("Could not generate a unique slug after 3 attempts.")

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.slug = self.generate_project_slug()

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

    @property
    def members(self):
        User = apps.get_model("calyvim", "User")
        return (
            User.objects.filter(user_board_permissions__board=self)
            .distinct()
            .order_by("first_name")
        )


class BoardTeamPermission(UUIDTimestampModel):
    board = models.ForeignKey(
        "Board", on_delete=models.CASCADE, related_name="team_memberships"
    )
    team = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="team_board_team_memberships"
    )
    role = models.CharField(
        max_length=20,
        choices=BoardPermissionRole.choices,
        default=BoardPermissionRole.COLLABORATOR,
    )

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

    board = models.ForeignKey(
        "Board", on_delete=models.CASCADE, related_name="permissions"
    )
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_board_permissions"
    )
    role = models.CharField(
        max_length=20,
        choices=BoardPermissionRole.choices,
        default=BoardPermissionRole.COLLABORATOR,
    )
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
