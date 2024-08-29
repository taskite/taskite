from rest_framework import permissions

from taskite.models import Board, WorkspaceMembership, BoardMembership


# class BoardViewPermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         board = request.board
#         organization = board.organization

#         # Check for organization permission
#         if not OrganizationUser.objects.filter(
#             organization=organization, user=request.user
#         ).exists():
#             return False

#         # Check for public board
#         if board.visibility == Board.Visibility.PUBLIC:
#             return True

#         # Check for board membership for private board
#         if not BoardMembership.objects.filter(board=board, user=request.user).exists():
#             return False

#         return True


# class BoardEditPermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         board = request.board
#         organization = board.organization

#         # Check for organization permission
#         if not OrganizationUser.objects.filter(
#             organization=organization, user=request.user
#         ).exists():
#             return False

#         # Check for board membership for private board
#         if not BoardMembership.objects.filter(board=board, user=request.user).exists():
#             return False

#         return True


class BoardPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        workspace = request.board.workspace

        workspace_membership = WorkspaceMembership.objects.filter(
            workspace=workspace, user=request.user
        ).first()
        if not workspace_membership:
            return False

        if workspace_membership.role == WorkspaceMembership.Role.ADMIN:
            return True

        board_membership = BoardMembership.objects.filter(
            board=request.board, user=request.user
        ).first()
        if not board_membership:
            return False

        return True
