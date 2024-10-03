from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND


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
    default_code = "no_team_membership_found"


class UserNotFoundException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "No user found."
    default_code = "no_user_found"


class BoardMembershipNotFoundException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "No board membership found."
    default_code = "no_board_membership_found"


class TaskNotFoundException(APIException):
    status_code = HTTP_404_NOT_FOUND
    default_detail = "No task found with the given task ID."
    default_code = "no_task_found"


class StateNotFoundException(APIException):
    status_code = HTTP_404_NOT_FOUND
    default_detail = "No state found with the given state ID."
    default_code = "no_state_found"


class PriorityNotFoundException(APIException):
    status_code = HTTP_404_NOT_FOUND
    default_detail = "No priority found with the given priority ID."
    default_code = "no_priority_found"