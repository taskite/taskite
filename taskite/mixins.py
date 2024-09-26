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