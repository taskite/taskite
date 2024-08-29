from taskite.models import Board
from taskite.exceptions import BoardNotFoundException


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