from __future__ import annotations

from typing import Protocol, runtime_checkable

from django.views.decorators.csrf import csrf_exempt
from rest_framework import exceptions, status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import BaseThrottle

from app.base.exceptions.handler import exception_handler
from app.base.models.base import BaseModel
from app.base.permissions.base import BasePermission
from app.base.serializers.base import BaseSerializer
from app.base.services.cache import Cacher
from app.base.utils.common import status_by_method
from app.base.utils.schema import extend_schema
from app.users.models import User

__all__ = ['BaseView']


class _RequestProtocol(Request):
    @property
    def user(self) -> User:
        return super().user()


class BaseView(GenericAPIView):
    request: _RequestProtocol

    many: bool = False
    serializer_class = BaseSerializer
    permission_classes = []
    serializer_map: dict[
        str, tuple[int, type[BaseSerializer]] | type[BaseSerializer]
    ] = {}
    permissions_map: dict[str, list[type[BasePermission]]] = {}
    throttle_map: dict[str, list[tuple[type[BaseThrottle], list[str]]]] = {}
    lookup_field = 'id'
    use_list_cache: bool = False
    list_cacher = Cacher('view_list', default={})
    list_cache_timeout = 30

    _method = ''

    @property
    def method(self) -> str:
        return self.request.method.lower() if hasattr(self, 'request') else self._method

    def list_cache(self, response: Response = None) -> Response:
        if self.use_list_cache:
            cache_key = type(self).__name__
            request_key = self.request.query_params.urlencode()
            cached_responses: dict = self.list_cacher.get(cache_key)
            cached_response: dict | None = cached_responses.get(request_key)
            if response is None:
                if cached_response:
                    return Response(**cached_response)
            else:
                self.list_cacher.set(
                    cached_responses
                    | {
                        request_key: {
                            'data': response.data,
                            'status': response.status_code,
                        }
                    },
                    cache_key,
                    timeout=self.list_cache_timeout,
                )
        return response

    @classmethod
    def invalidate_list_cache(cls, **kwargs) -> None:
        cls.list_cacher.delete(cls.__name__)

    @classmethod
    def _extract_serializer_class_with_status(
        cls, method_name: str
    ) -> tuple[int, type[BaseSerializer]] | None:
        serializer_class = cls.serializer_map.get(method_name)
        if (
            serializer_class
            and not isinstance(serializer_class, tuple)
            and issubclass(serializer_class, BaseSerializer)
        ):
            http_status = status_by_method(method_name)
            return http_status, serializer_class
        return serializer_class

    def get_serializer_class(self) -> type[BaseSerializer]:
        serializer_class = self._extract_serializer_class_with_status(self.method)
        if serializer_class is None:
            return self.serializer_class
        return serializer_class[1]

    def get_serializer(self, *args, **kwargs) -> BaseSerializer:
        return super().get_serializer(*args, **kwargs)

    def get_valid_serializer(self, *args, **kwargs) -> BaseSerializer:
        kwargs.setdefault('data', self.get_data())
        serializer = self.get_serializer(*args, **kwargs)
        serializer.is_valid()
        return serializer

    def get_object(self) -> BaseModel:
        return super().get_object()

    def get_permission_classes(self) -> list[type[BasePermission]]:
        return self.permission_classes + self.permissions_map.get(self.method, [])

    def get_permissions(self) -> list[BasePermission]:
        return [p() for p in self.get_permission_classes()]

    def get_throttles(self):
        throttles = super().get_throttles()
        if throttle_confs := self.throttle_map.get(self.method):
            for throttle_class, throttle_rates in throttle_confs:
                throttles += [
                    type(
                        '_',
                        (throttle_class,),
                        {
                            'rate': rate,
                            'scope': f"{self.__class__.__name__}_{self.method}",
                        },
                    )()
                    for rate in throttle_rates
                ]
        return throttles

    @classmethod
    def _decorate_methods(cls) -> None:
        def _force_args(f):
            def wrapped_f(*args, **kwargs):
                if f.__name__ != 'wrapped_f':
                    match f.__code__.co_argcount:
                        case 0:
                            return f()
                        case 1:
                            return f(args[0])
                return f(*args, **kwargs)

            for key, value in f.__dict__.items():
                setattr(wrapped_f, key, value)
            return wrapped_f

        self = cls()
        for method_name in cls.http_method_names:
            try:
                method = getattr(cls, method_name)
            except AttributeError:
                continue
            self._method = method_name
            responses = {}

            extracted = cls._extract_serializer_class_with_status(method_name)
            if extracted:
                serializer_class = extracted[1]
                if get_schema := getattr(serializer_class, 'get_schema'):
                    responses |= get_schema(extracted[0])

            auth = [{}]
            if any(map(lambda p: p.requires_authentication, cls.get_permissions(self))):
                auth = [{'Cookie': []}, {'jwtAuth': []}]

            method = _force_args(method)
            method = extend_schema(responses=responses, auth=auth)(method)
            setattr(cls, method_name, method)

    @classmethod
    def as_view(cls, **init_kwargs):
        if cls.many:
            cls.__bases__ += (ListModelMixin,)
        cls._decorate_methods()
        return csrf_exempt(super().as_view(**init_kwargs))

    def handle_exception(self, exception):
        return exception_handler(exception)

    def permission_denied(self, request, message=None, code=None):
        if request.authenticators and not request.successful_authenticator:
            getattr(request, 'on_auth_fail', lambda: None)()
            raise exceptions.NotAuthenticated()
        raise exceptions.PermissionDenied(detail=message, code=code)

    def get_data(self) -> dict:
        return self.request.data

    def list(self):
        if cached_response := self.list_cache():
            return cached_response
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.list_cache(self.get_paginated_response(serializer.data))
        serializer = self.get_serializer(queryset, many=True)
        return self.list_cache(Response(serializer.data))

    def create(self, **kwargs):
        serializer = self.get_valid_serializer()
        serializer.save(**kwargs)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self):
        instance = self.get_object()
        serializer = self.get_valid_serializer(instance, partial=True)
        serializer.save()

    def destroy(self):
        instance = self.get_object()
        instance.delete()
