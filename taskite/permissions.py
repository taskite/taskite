from rest_framework import permissions

from taskite.models import Board, OrganizationUser, BoardMembership


class BoardViewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        board = request.board
        organization = board.organization

        # Check for organization permission
        if not OrganizationUser.objects.filter(
            organization=organization, user=request.user
        ).exists():
            return False

        # Check for public board
        if board.visibility == Board.Visibility.PUBLIC:
            return True

        # Check for board membership for private board
        if not BoardMembership.objects.filter(board=board, user=request.user).exists():
            return False

        return True
