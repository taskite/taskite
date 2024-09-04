from django.db import models
from django.urls import reverse
from django.conf import settings

from taskite.models.base import UUIDTimestampModel


class Workspace(UUIDTimestampModel):
    name = models.CharField(
        max_length=124,
        help_text="This is the name of your company, team or organization.",
    )
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        "User", on_delete=models.SET_NULL, null=True, related_name="created_workspaces"
    )

    members = models.ManyToManyField(
        "User", through="WorkspaceMembership", related_name="workspaces"
    )

    class Meta:
        db_table = "workspaces"

    def __str__(self) -> str:
        return self.name


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
    accepted = models.BooleanField(default=False)

    class Meta:
        db_table = "workspace_invites"
        verbose_name = "Workspace Invite"
        verbose_name_plural = "Workspace Invites"

    def __str__(self) -> str:
        return self.email

    @property
    def confirmation_link(self):
        return settings.BASE_URL + reverse("invite-workspace-confirm", args=[self.id])

    @property
    def rejection_link(self):
        return settings.BASE_URL + reverse("invite-workspace-reject", args=[self.id])
