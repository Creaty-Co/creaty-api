from __future__ import annotations

from collections.abc import Callable
from typing import Any

from django.conf import settings
from rest_framework.response import Response

from base.logs import error

__all__ = ['APIException', 'CastSupportsError']


class APIException(Exception):
    TYPE_NAME: str

    def __init__(self, code: str, detail: str, status: int):
        self.detail: str = detail
        self.status: int = status
        self.code: str = code

    def serialize(self) -> dict[str, dict[str, Any]]:
        if settings.DEBUG or settings.TEST:
            return {
                'error': {
                    'type': self.TYPE_NAME,
                    'detail': self.detail,
                    'code': self.code,
                }
            }
        return {'error': {'type': self.TYPE_NAME, 'code': self.code}}

    def to_response(self) -> Response:
        return Response(data=self.serialize(), status=self.status)


class LoggedException(APIException):
    LOG_FUNC = error

    def __init__(self, code, detail, status, log_func=None):
        super().__init__(code, detail, status)
        self.log_func = log_func or self.LOG_FUNC

    def log(self) -> None:
        self.log_func(self.detail)


class CastSupportsError(LoggedException):
    EXCEPTION__CAST: dict[type[Exception], Callable[[Exception], APIException]] = {}

    @classmethod
    def cast_exception(cls, exception: Exception) -> APIException:
        for exception_type, caster in cls.EXCEPTION__CAST.items():
            if issubclass(type(exception), exception_type):
                return caster(exception)
        raise ValueError(f'Casting is not supported for {type(exception)}')
