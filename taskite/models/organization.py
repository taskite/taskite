import uuid
from django.db import models


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=124)
    created_by = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)
    logo = models.ImageField(blank=True, null=True, upload_to="organizations/logos/")
    boards_count = models.IntegerField(default=0)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "organizations"

    def __str__(self) -> str:
        return self.name


class OrganizationUser(models.Model):
    class Role(models.TextChoices):
        OWNER = ("owner", "Owner")
        ADMIN = ("admin", "Admin")
        STAFF = ("staff", "Staff")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, related_name="users"
    )
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STAFF)

    # Timestamp
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "organization_users"
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "user"], name="unique_user_per_organization"
            )
        ]

    def __str__(self) -> str:
        return str(self.id)
