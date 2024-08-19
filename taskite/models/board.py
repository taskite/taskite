import uuid
from django.db import models


class Board(models.Model):
    class Visibility(models.TextChoices):
        PUBLIC = ("public", "Public")
        PRIVATE = ("private", "Private")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        "Organization", related_name="boards", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=124)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)
    visibility = models.CharField(
        max_length=10, choices=Visibility.choices, default=Visibility.PRIVATE
    )
    cover = models.ImageField(blank=True, null=True, upload_to="boards/covers/")
    task_number_counter = models.IntegerField(default=1)
    task_prefix = models.CharField(max_length=5, blank=True)
    tasks_count = models.IntegerField(default=0)
    members_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived_at = models.DateTimeField(blank=True, null=True)

    members = models.ManyToManyField(
        "User", through="BoardMembership", related_name="boards"
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "boards"

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding:
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


class BoardMembership(models.Model):
    class Role(models.TextChoices):
        ADMIN = ("admin", "Admin")
        STAFF = ("staff", "Staff")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    board = models.ForeignKey(
        "Board", on_delete=models.CASCADE, related_name="memberships"
    )
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="board_memberships"
    )
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STAFF)

    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "board_memberships"
        constraints = [
            models.UniqueConstraint(
                fields=["board", "user"], name="unique_member_per_board"
            )
        ]

    def __str__(self) -> str:
        return str(self.id)
