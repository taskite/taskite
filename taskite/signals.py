from django.db.models.signals import post_save
from django.dispatch import receiver

from taskite.models import (
    OrganizationUser,
    Organization,
    Board,
    State,
    Priority,
    BoardMembership,
)


@receiver(post_save, sender=Organization)
def create_organization_owner(sender, instance, created, **kwargs):
    if created:
        OrganizationUser.objects.create(
            organization=instance,
            user=instance.created_by,
            role=OrganizationUser.Role.OWNER,
        )


@receiver(post_save, sender=Board)
def create_board_admin(sender, instance, created, **kwargs):
    if created:
        BoardMembership.objects.create(
            board=instance, user=instance.created_by, role=BoardMembership.Role.ADMIN
        )


@receiver(post_save, sender=Board)
def setup_initial_project(sender, instance, created, **kwargs):
    if created:
        # 1. Creating initial set of states
        State.objects.bulk_create(
            [
                State(board=instance, name="Backlog", sequence=10000),
                State(board=instance, name="Todo", sequence=20000),
                State(board=instance, name="In-progress", sequence=30000),
                State(board=instance, name="Review", sequence=40000),
                State(board=instance, name="Done", sequence=50000),
            ]
        )

        # 2. Creating initial set of priorities
        Priority.objects.bulk_create(
            [
                Priority(board=instance, name="Urgent"),
                Priority(board=instance, name="High"),
                Priority(board=instance, name="Medium"),
                Priority(board=instance, name="Low"),
            ]
        )
