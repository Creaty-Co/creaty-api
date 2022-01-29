import string
from typing import Final

from django.http import Http404
from drf_spectacular.utils import OpenApiResponse
from rest_framework import serializers, status as rest_status
from rest_framework.exceptions import (
    APIException as RestAPIException,
    AuthenticationFailed, NotFound, Throttled
)

from base.exceptions.base import *
from base.exceptions.utils import extract_detail
from base.logs import warning
from base.serializers.base import BaseSerializer

__all__ = ['APIWarning']


def _cast_rest_api_exception(exception: RestAPIException):
    return APIWarning(
        extract_detail(exception), getattr(exception, 'status_code'),
        exception.get_codes()
    )


def _cast_404(exception: Http404):
    return APIWarning(str(exception), rest_status.HTTP_404_NOT_FOUND, ['not_found'])


class APIWarning(CastSupportsError):
    TYPE_NAME = 'warning'
    LOG_FUNC = warning
    
    EXCEPTION__CAST = {
        AuthenticationFailed: _cast_rest_api_exception,
        Throttled: _cast_rest_api_exception,
        Http404: _cast_404,
        NotFound: _cast_404
    }
    
    __schema_cache = {}
    
    def __init__(self, detail=None, status=None, codes: list[str] = None):
        super().__init__(
            detail or 'Warning', status or rest_status.HTTP_423_LOCKED
        )
        self.codes: Final[list[str]] = codes or []
    
    def serialize(self):
        json = super().serialize()
        if self.codes:
            json['error']['codes'] = self.codes
        return json
    
    def to_schema(self, serializer_name: str = None):
        if serializer_name is None:
            serializer_name = ''
            for code in self.codes:
                serializer_name += string.capwords(code, sep='_').replace('_', '')
        try:
            serializer = self.__schema_cache[serializer_name]
        except KeyError:
            serializer = type(
                serializer_name, (BaseSerializer,), {
                    'error': serializers.DictField(
                        default={'type': self.TYPE_NAME, 'codes': self.codes},
                        read_only=True
                    )
                }
            )
            self.__schema_cache[serializer_name] = serializer
        return OpenApiResponse(
            response=serializer,
            description='\t' + self.detail
        )
