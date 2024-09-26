from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.db import models

from taskite.models import (
    Workspace,
    WorkspaceMembership,
    Board,
    State,
    Priority,
    BoardMembership,
    Upload,
)


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


# def confirm_upload(file_path):
#     if default_storage.exists(file_path):
#         print(f"File {file_path} confirmed")
#     else:
#         print(f"File {file_path} not found")


# def mark_file_as_deleted(file_path):
#     print(f"File {file_path} marked as deleted")


# def get_file_fields(instance):
#     return [
#         field for field in instance._meta.fields if isinstance(field, models.FileField)
#     ]


# @receiver(pre_save)
# def cache_original_file_fields(sender, instance, **kwargs):
#     if instance.pk:  # Only cache for existing instances
#         instance._original_file_fields = {}
#         for field in get_file_fields(instance):
#             original_file = getattr(instance, field.name)
#             if original_file:
#                 instance._original_file_fields[field.name] = original_file.name

#         print('Original Map ->', instance._original_file_fields)


# @receiver(post_save)
# def handle_file_operations_on_save(sender, instance, created, **kwargs):
#     file_fields = get_file_fields(instance)

#     if not file_fields:
#         return  # No file fields in this model, so we don't need to do anything

#     if created:
#         # New instance created
#         for field in file_fields:
#             file_instance = getattr(instance, field.name)
#             if file_instance:
#                 confirm_upload(file_instance.name)
#     else:
#         # Instance being updated
#         original_fields = getattr(instance, "_original_file_fields", {})
#         for field in file_fields:
#             current_file = getattr(instance, field.name)
#             original_file_name = original_fields.get(field.name)

#             if current_file and current_file.name != original_file_name:
#                 # New file uploaded or changed
#                 confirm_upload(current_file.name)
#                 if original_file_name:
#                     mark_file_as_deleted(original_file_name)
#             elif not current_file and original_file_name:
#                 # File was removed
#                 mark_file_as_deleted(original_file_name)


# @receiver(post_delete)
# def handle_file_operations_on_delete(sender, instance, **kwargs):
#     for field in get_file_fields(instance):
#         file_instance = getattr(instance, field.name)
#         if file_instance:
#             mark_file_as_deleted(file_instance.name)
