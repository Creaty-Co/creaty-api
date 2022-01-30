from django.http import Http404
from rest_framework import status as rest_status
from rest_framework.exceptions import (
    MethodNotAllowed, NotAuthenticated, NotFound, ParseError, PermissionDenied,
    UnsupportedMediaType, ValidationError as RestValidationError
)

from base.exceptions.base import *
from base.exceptions.utils import client_error_cast_rest_api_exception

__all__ = ['ClientError']


def _cast_404(exception):
    return ClientError(str(exception), rest_status.HTTP_404_NOT_FOUND, 'not_found')


class ClientError(CastSupportsError):
    TYPE_NAME = 'error'
    
    EXCEPTION__CAST = {
        RestValidationError: client_error_cast_rest_api_exception,
        ParseError: client_error_cast_rest_api_exception,
        NotAuthenticated: client_error_cast_rest_api_exception,
        PermissionDenied: client_error_cast_rest_api_exception,
        NotFound: client_error_cast_rest_api_exception,
        Http404: _cast_404,
        MethodNotAllowed: client_error_cast_rest_api_exception,
        UnsupportedMediaType: client_error_cast_rest_api_exception,
    }
    
    def __init__(self, detail=None, status=None, code=None):
        super().__init__(
            code or 'invalid', detail or 'Client error',
            status or rest_status.HTTP_400_BAD_REQUEST
        )
