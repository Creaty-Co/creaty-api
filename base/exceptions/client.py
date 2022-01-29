from rest_framework import status as rest_status
from rest_framework.exceptions import (
    APIException as RestAPIException, MethodNotAllowed, NotAuthenticated, NotFound,
    ParseError, PermissionDenied, UnsupportedMediaType,
    ValidationError as RestValidationError
)

from base.exceptions.base import *

__all__ = ['ClientError']

from base.exceptions.utils import extract_detail


def _cast_rest_api_exception(exception: RestAPIException):
    return ClientError(extract_detail(exception), getattr(exception, 'status_code'))


def _cast_rest_validation_error(exception: RestValidationError):
    return ClientError(extract_detail(exception), getattr(exception, 'status_code'))


class ClientError(CastSupportsError):
    TYPE_NAME = 'client_error'
    
    EXCEPTION__CAST = {
        RestValidationError: _cast_rest_validation_error,
        ParseError: _cast_rest_api_exception,
        NotAuthenticated: _cast_rest_api_exception,
        PermissionDenied: _cast_rest_api_exception,
        NotFound: _cast_rest_api_exception,
        MethodNotAllowed: _cast_rest_api_exception,
        UnsupportedMediaType: _cast_rest_api_exception,
    }
    
    def __init__(self, detail=None, status=None):
        super().__init__(
            detail or 'Client error', status or rest_status.HTTP_400_BAD_REQUEST
        )
