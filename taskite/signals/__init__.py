from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


from taskite.models import (
    Workspace,
    WorkspaceMembership,
    Board,
    State,
    Priority,
    BoardPermission,
    BoardTeamPermission,
)
from taskite.tasks import file_archive


@receiver(post_save, sender=Workspace)
def create_default_workspace(sender, instance, created, **kwargs):
    if created:
        WorkspaceMembership.objects.create(
            workspace=instance,
            user=instance.created_by,
            role=WorkspaceMembership.Role.ADMIN,
        )


@receiver(post_save, sender=Board)
def create_board_admin(sender, instance, created, **kwargs):
    if created:
        workspace_membership = WorkspaceMembership.objects.filter(
            user=instance.created_by, workspace=instance.workspace
        ).first()

        if not workspace_membership:
            raise ObjectDoesNotExist("No membership found for the user")

        BoardPermission.objects.create(
            board=instance,
            user=instance.created_by,
            role="admin",
            workspace_membership=workspace_membership,
        )


@receiver(post_save, sender=BoardTeamPermission)
def create_or_update_board_permission(sender, instance, created, **kwargs):
    if created:
        team_memberships = instance.team.memberships.all()
        for team_membership in team_memberships:
            BoardPermission.objects.create(
                board=instance.board,
                role=instance.role,
                team_permission=instance,
                team_membership=team_membership,
                user=team_membership.user,
            )
    else:
        BoardPermission.team_objects.filter(
            board=instance.board, team_permission=instance
        ).update(role=instance.role)


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


def get_file_fields(instance):
    return [
        field for field in instance._meta.fields if isinstance(field, models.FileField)
    ]





@receiver(post_delete)
def handle_file_operations_on_delete(sender, instance, **kwargs):
    for field in get_file_fields(instance):
        file_instance = getattr(instance, field.name)
        if file_instance:
            file_archive.delay(file_instance.name)
