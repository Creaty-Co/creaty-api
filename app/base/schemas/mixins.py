from typing import Any

from drf_spectacular.utils import OpenApiResponse

from app.base.exceptions import APIWarning

__all__ = ['SerializerSchemaMixin', 'ViewSchemaMixin']


class SerializerSchemaMixin:
    WARNINGS: dict[Any, APIWarning] = {}
    _DESCRIPTION = None

    @classmethod
    def get_schema(cls, success_status: int = 200) -> dict[int, OpenApiResponse]:
        if cls._DESCRIPTION is None:
            description = None
        else:
            description = '\t' + cls._DESCRIPTION
        return {success_status: OpenApiResponse(cls, description=description)} | {
            warning.status: warning.get_schema() for warning in cls.WARNINGS.values()
        }


class ViewSchemaMixin:
    WARNINGS: dict[Any, APIWarning] = {}

    @classmethod
    def get_schema(cls) -> dict[int, OpenApiResponse]:
        return {
            warning.status: warning.get_schema() for warning in cls.WARNINGS.values()
        }
