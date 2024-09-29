from django.db import models

from taskite.models.base import UUIDTimestampModel


class Team(UUIDTimestampModel):
    workspace = models.ForeignKey(
        "Workspace", related_name="teams", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=124)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(
        "User", through="TeamMembership", related_name="teams"
    )
    avatar = models.ImageField(blank=True, null=True, upload_to="attachments/")

    class Meta:
        db_table = "teams"

    def __str__(self) -> str:
        return self.name


class TeamMembership(UUIDTimestampModel):
    team = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="memberships"
    )
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="team_memberships"
    )

    class Meta:
        db_table = "team_memberships"
        constraints = [
            models.UniqueConstraint(
                fields=["team", "user"], name="unique_user_per_team"
            )
        ]

    def __str__(self) -> str:
        return str(self.id)
