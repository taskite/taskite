from django.db import models, transaction
from django.urls import reverse
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.utils import timezone

from taskite.models.base import UUIDTimestampModel


class ActiveWorkspaceManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class Workspace(UUIDTimestampModel):
    name = models.CharField(
        max_length=124,
        help_text="This is the name of your company, team or organization.",
    )
    slug = models.SlugField(max_length=124, blank=True, unique=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        "User", on_delete=models.SET_NULL, null=True, related_name="created_workspaces"
    )
    logo = models.ImageField(blank=True, null=True, upload_to="attachments/")
    org_size = models.CharField(max_length=20, default="1")

    members = models.ManyToManyField(
        "User", through="WorkspaceMembership", related_name="workspaces"
    )

    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "workspaces"

    objects = ActiveWorkspaceManager()
    all_objects = models.Manager()

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.slug:
                self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    @transaction.atomic
    def soft_delete(self):
        self.slug = f"{self.slug}-deleted-{get_random_string(12)}"
        self.deleted_at = timezone.now()
        self.save(update_fields=["slug", "deleted_at"])


class WorkspaceMembership(UUIDTimestampModel):
    class Role(models.TextChoices):
        ADMIN = ("admin", "Admin")
        COLLABORATOR = ("collaborator", "Collaborator")
        GUEST = ("guest", "Guest")

    workspace = models.ForeignKey(
        "Workspace", on_delete=models.CASCADE, related_name="memberships"
    )
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="workspace_memberships"
    )
    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.COLLABORATOR
    )

    class Meta:
        db_table = "workspace_memberships"
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "user"], name="unqiue_user_per_workspace"
            )
        ]

    def __str__(self) -> str:
        return str(self.id)


class WorkspaceInvite(UUIDTimestampModel):
    workspace = models.ForeignKey(
        "Workspace", on_delete=models.CASCADE, related_name="invites"
    )
    email = models.EmailField()
    invited_by = models.ForeignKey(
        "User", on_delete=models.SET_NULL, null=True, related_name="sent_invites"
    )
    confirmed_at = models.DateTimeField(blank=True, null=True)
    invitation_id = models.CharField(max_length=64, blank=True, null=True, unique=True)

    class Meta:
        db_table = "workspace_invites"
        verbose_name = "Workspace Invite"
        verbose_name_plural = "Workspace Invites"

    def __str__(self) -> str:
        return self.email

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.invitation_id:
                self.invitation_id = get_random_string(64)
        return super().save(*args, **kwargs)

    def confirm_invitation(self):
        self.confirmed_at = timezone.now()
        self.invitation_id = None
        self.save(update_fields=["confirmed_at", "invitation_id"])

    @property
    def confirmation_link(self):
        if not self.invitation_id:
            self.invitation_id = get_random_string(64)
            self.save(update_fields=["invitation_id"])

        return settings.BASE_URL + reverse(
            "workspaces-member-confirmation",
            args=[self.workspace.slug, self.invitation_id],
        )
