from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED


class InvalidInputException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "Invalid input provided."
    default_code = "invalid_input"


class WorkspaceNotFoundException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "No workspace found."
    default_code = "no_workspace_found"


class WorkspaceInvalidPermission(APIException):
    status_code = HTTP_401_UNAUTHORIZED
    default_detail = "You don't have enough permission to perform this action."
    default_code = "no_workspace_permission_found"


class BoardInvalidPermission(APIException):
    status_code = HTTP_401_UNAUTHORIZED
    default_detail = "You don't have enough permission to perform this action."
    default_code = "no_board_permission_found"


class BoardNotFoundException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "No board found."
    default_code = "no_board_found"


class WorkspaceMembershipNotFoundException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "No workspace membership found."
    default_code = "no_workspace_membership_found"


class WorkspaceInviteNotFoundException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "No workspace invite found."
    default_code = "no_workspace_invite_found"


class TeamNotFoundException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "No team found."
    default_code = "no_team_found"


class MemberNotFoundException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "No member found"
    default_code = "no_member_found"


class TeamMembershipNotFoundEception(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "No team membership found"
    default_code = "no_team_membershio_found"