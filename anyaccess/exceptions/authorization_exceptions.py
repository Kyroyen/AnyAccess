from rest_framework.exceptions import APIException

class WrongTokenTypeException(APIException):
    status_code = 401
    default_detail = 'Wrong token type'