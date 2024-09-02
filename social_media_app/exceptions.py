from rest_framework.serializers import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework import status


class CustomException(Exception):
    def __init__(self, detail, status_code: int=None):
        self.detail = detail

        if status_code != None:
            self.status_code = status_code


class CustomValidation(ValidationError):
    def __init__(self, detail: str, status_code: int=None):
        self.detail = detail

        if status_code != None:
            self.status_code = status_code

class CustomPermissionException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _("You do not have permission to perform this action.")
    default_message = "Permission denied"

    def __init__(self, detail=None):
        if detail is None:
            detail = self.default_detail
        
        self.detail = {
            "hasError": True,
            "errorCode": self.status_code,
            "message": detail,
            "debugMessage": self.default_message,
            "response":{}
        }