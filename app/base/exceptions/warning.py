from django.utils.crypto import get_random_string
from drf_spectacular.utils import OpenApiResponse
from rest_framework import serializers
from rest_framework import status as rest_status
from rest_framework.exceptions import APIException as RestAPIException
from rest_framework.exceptions import AuthenticationFailed, Throttled

from app.base.exceptions.base import CastSupportsError
from app.base.exceptions.utils import extract_detail
from app.base.logs import warning

__all__ = ['APIWarning']


def _cast_rest_api_exception(exception: RestAPIException):
    return APIWarning(
        extract_detail(exception),
        getattr(exception, 'status_code'),
        '_'.join(map(str, exception.get_codes())),
    )


class APIWarning(CastSupportsError):
    TYPE_NAME = 'warning'
    LOG_FUNC = warning

    EXCEPTION__CAST = {
        AuthenticationFailed: _cast_rest_api_exception,
        Throttled: _cast_rest_api_exception,
    }

    __schema_cache = {}

    def __init__(self, detail=None, status=None, code: str = None):
        super().__init__(detail or 'Warning', status or rest_status.HTTP_423_LOCKED)
        self.code: str | None = code

    def serialize(self):
        json = super().serialize()
        if self.code:
            json['error']['code'] = self.code
        return json

    def get_schema(self, serializer_name: str = None) -> OpenApiResponse:
        from app.base.serializers.base import BaseSerializer

        if serializer_name is None:
            if self.code:
                serializer_name = self.code.capitalize()
            else:
                serializer_name = get_random_string(5)
        try:
            serializer = self.__schema_cache[serializer_name]
        except KeyError:
            serializer = type(
                serializer_name,
                (BaseSerializer,),
                {
                    'error': serializers.DictField(
                        default={'type': self.TYPE_NAME, 'code': self.code},
                        read_only=True,
                    )
                },
            )
            self.__schema_cache[serializer_name] = serializer
        return OpenApiResponse(response=serializer, description='\t' + self.detail)
