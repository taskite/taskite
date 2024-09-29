from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.db import models
from django.utils import timezone
from datetime import datetime

from taskite.models import (
    Workspace,
    WorkspaceMembership,
    Board,
    State,
    Priority,
    BoardMembership,
)
from taskite.tasks import purge_asset, remove_unused_asset


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


def get_file_fields(instance):
    return [
        field for field in instance._meta.fields if isinstance(field, models.FileField)
    ]


@receiver(pre_save)
def cache_original_file_fields(sender, instance, update_fields=None, **kwargs):
    if sender.__name__ == "PurgeAsset" or sender.__name__ == "UnusedAsset":
        return

    if instance._state.adding:
        return

    # Only cache for existing instances
    instance._original_file_fields = {}
    file_fields = get_file_fields(instance)

    if not file_fields:
        return

    # If update_fields is provided, only consider file fields that are being updated
    if update_fields:
        file_fields = [field for field in file_fields if field.name in update_fields]

    if not file_fields:
        return

    file_field_names = [field.name for field in file_fields]

    original_instance = sender.objects.only("pk", *file_field_names).get(pk=instance.pk)
    for field in file_fields:
        original_file = getattr(original_instance, field.name)
        if original_file:
            instance._original_file_fields[field.name] = original_file.name


@receiver(post_save)
def handle_file_operations_on_save(sender, instance, created, **kwargs):
    if sender.__name__ == "PurgeAsset" or sender.__name__ == "UnusedAsset":
        return

    file_fields = get_file_fields(instance)

    if not file_fields:
        return  # No file fields in this model, so we don't need to do anything

    if created:
        for field in file_fields:
            file_instance = getattr(instance, field.name)
            if file_instance:
                # New record has file fields
                # confirm_upload.delay(file_instance.name)
                remove_unused_asset.delay(file_instance.name)
    else:
        # Instance being updated
        original_fields = getattr(instance, "_original_file_fields", {})
        for field in file_fields:
            current_file = getattr(instance, field.name)
            original_file_name = original_fields.get(field.name)

            if current_file and current_file.name != original_file_name:
                # New file uploaded or changed
                # confirm_upload.delay(current_file.name)
                remove_unused_asset.delay(current_file.name)

                if original_file_name:
                    # Delete the old file
                    # mark_file_as_deleted.delay(original_file_name)
                    purge_asset.delay(original_file_name, datetime.now().isoformat())
            elif not current_file and original_file_name:
                # File was removed
                # mark_file_as_deleted.delay(original_file_name)
                purge_asset.delay(original_file_name, datetime.now().isoformat())


@receiver(post_delete)
def handle_file_operations_on_delete(sender, instance, **kwargs):
    for field in get_file_fields(instance):
        file_instance = getattr(instance, field.name)
        if file_instance:
            # mark_file_as_deleted.delay(file_instance.name)
            purge_asset.delay(file_instance.name, datetime.now().isoformat())
