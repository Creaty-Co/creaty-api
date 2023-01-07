from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status as rest_status
from rest_framework.exceptions import APIException as RestAPIException

from app.base.exceptions.base import CastSupportsError
from app.base.exceptions.utils import extract_detail
from app.base.logs import critical

__all__ = ['CriticalError']


def _cast_rest_api_exception(exception: RestAPIException):
    return CriticalError(extract_detail(exception), getattr(exception, 'status_code'))


def _cast_django_validation_error(exception: DjangoValidationError):
    if (message := getattr(exception, 'error_dict', None)) is None:
        if (message := getattr(exception, 'error_list', None)) is None:
            message = exception.message
    return CriticalError(message)


def _cast_exception(exception: Exception):
    return CriticalError(str(exception))


class CriticalError(CastSupportsError):
    TYPE_NAME = 'critical_error'
    LOG_FUNC = critical

    EXCEPTION__CAST = {
        RestAPIException: _cast_rest_api_exception,
        DjangoValidationError: _cast_django_validation_error,
        Exception: _cast_exception,
    }

    def __init__(self, detail=None, status=None):
        super().__init__(
            detail or 'Server error',
            status or rest_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
