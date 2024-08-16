from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST


class InvalidInputException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "Invalid input provided."
    default_code = "invalid_input"
