from rest_framework import serializers
from taskite.models import Board, Workspace
from taskite.exceptions import BoardNotFoundException, WorkspaceNotFoundException


class FileUploadMixin:
    def save(self, *args, **kwargs):
        # Call the original save() method to actually save the instance
        super().save(*args, **kwargs)


class BoardMixin:
    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)
        board_id = kwargs.get("board_id")
        if board_id:
            board = Board.objects.filter(id=board_id).first()
            if not board:
                raise BoardNotFoundException
            request.board = board
        return request


class WorkspaceMixin:
    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)
        workspace_id = kwargs.get("workspace_id")
        if workspace_id:
            workspace = Workspace.objects.filter(id=workspace_id).first()
            if not workspace:
                raise WorkspaceNotFoundException
            request.workspace = workspace
        return request


class FileNameAndSourceSerializerMixin:
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field_name, field in self.fields.items():
            if isinstance(field, serializers.FileField):
                field_value = getattr(instance, field_name)
                if field_value:
                    # Set the original field to the filename
                    representation[field_name] = field_value.name
                    # Add a new field with 'Src' suffix containing the URL
                    representation[f"{field_name}_src"] = field_value.url
                else:
                    # If the field is empty, set both fields to None
                    representation[field_name] = None
                    representation[f"{field_name}_src"] = None
        return representation


class NameAndSourceSerializerMixin:
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field_name, field in self.fields.items():
            if isinstance(field, serializers.FileField):
                field_value = getattr(instance, field_name)
                if field_value:
                    # Set the original field to the filename
                    representation[field_name] = field_value.name
                    # Add a new field with 'Src' suffix containing the URL
                    representation[f"{field_name}_src"] = field_value.url
                else:
                    # If the field is empty, set both fields to None
                    representation[field_name] = None
                    representation[f"{field_name}_src"] = None
        return representation