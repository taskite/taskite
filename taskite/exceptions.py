from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST


class InvalidInputException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "Invalid input provided."
    default_code = "invalid_input"


class OrganizationNotFoundException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "No organization found."
    default_code = "no_organization_found"


class BoardNotFoundException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "No board found."
    default_code = "no_board_found"
