import string

from drf_spectacular.utils import OpenApiResponse
from rest_framework import serializers, status as rest_status
from rest_framework.exceptions import Throttled

from base.exceptions.base import *
from base.exceptions.utils import warning_cast_rest_api_exception
from base.logs import warning
from base.serializers.base import BaseSerializer

__all__ = ['APIWarning']


class APIWarning(CastSupportsError):
    TYPE_NAME = 'warning'
    LOG_FUNC = warning

    EXCEPTION__CAST = {Throttled: warning_cast_rest_api_exception}

    __schema_cache = {}

    def __init__(self, code, detail=None, status=None):
        assert code is not None
        super().__init__(
            code, detail or 'Warning', status or rest_status.HTTP_423_LOCKED
        )

    def to_schema(self, serializer_name: str = None):
        if serializer_name is None:
            serializer_name = ''
            for code in self.code:
                serializer_name += string.capwords(code, sep='_').replace('_', '')
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
