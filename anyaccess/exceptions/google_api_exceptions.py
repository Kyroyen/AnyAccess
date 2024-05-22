from rest_framework.exceptions import APIException

class GoogleAPITokenException(APIException):
    status_code = 401
    default_detail = 'Not the right type of token'