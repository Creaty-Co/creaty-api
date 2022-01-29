from __future__ import annotations

from typing import Type

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import set_rollback
from rest_framework.viewsets import ViewSetMixin

from base.exceptions import *
from base.schemas.mixins import SerializerSchemaMixin, ViewSchemaMixin
from base.serializers.base import EmptySerializer
from base.utils import status_by_method

__all__ = ['BaseView', 'BaseViewSet']


def _exception_handler(exception):
    try:
        set_rollback()
        if settings.DEBUG and isinstance(exception, MethodNotAllowed):
            return Response(str(exception))
        try:
            raise exception
        except APIWarning as e:
            api_error = e
        except ClientError as e:
            api_error = e
        except CriticalError as e:
            api_error = e
        except tuple(APIWarning.EXCEPTION__CAST.keys()) as exception_to_cast:
            api_error = APIWarning.cast_exception(exception_to_cast)
        except tuple(ClientError.EXCEPTION__CAST.keys()) as exception_to_cast:
            api_error = ClientError.cast_exception(exception_to_cast)
        except tuple(CriticalError.EXCEPTION__CAST.keys()) as exception_to_cast:
            api_error = CriticalError.cast_exception(exception_to_cast)
        
        error = api_error
    
    except Exception as e:
        error = CriticalError(str(e))
    
    error.log()
    return error.to_response()


class BaseView(GenericAPIView):
    lookup_field = 'id'
    ordering = 'id'
    serializer_class = EmptySerializer
    serializer_classes: dict[
        str, tuple[int, Type[serializers.Serializer]] | Type[serializers.Serializer]
    ] = {}
    
    @classmethod
    def _extract_serializer_class_with_status(
        cls, method_name: str
    ) -> tuple[int, Type[serializers.Serializer]] | None:
        serializer_class = cls.serializer_classes.get(method_name)
        if serializer_class and issubclass(serializer_class, serializers.Serializer):
            status = status_by_method(method_name)
            return status, serializer_class
        return serializer_class
    
    def get_serializer_class(self):
        serializer_class = self._extract_serializer_class_with_status(
            self.request.method.lower()
        )
        if serializer_class is None:
            return self.serializer_class
        return serializer_class[1]
    
    @classmethod
    def _to_schema(cls, clazz: Type[BaseView]) -> None:
        for method_name in clazz.http_method_names:
            try:
                method = getattr(clazz, method_name)
            except AttributeError:
                continue
            responses = {}
            
            extracted = clazz._extract_serializer_class_with_status(method_name)
            if extracted:
                serializer_class = extracted[1]
                if issubclass(serializer_class, SerializerSchemaMixin):
                    responses |= serializer_class.to_schema(extracted[0])
            
            if issubclass(clazz, ViewSchemaMixin):
                responses |= clazz.to_schema()
            
            setattr(clazz, method_name, extend_schema(responses=responses)(method))
    
    @classmethod
    def as_view(cls, **initkwargs):
        cls._to_schema(cls)
        return csrf_exempt(super().as_view(**initkwargs))
    
    def handle_exception(self, exception):
        return _exception_handler(exception)


class BaseViewSet(ViewSetMixin, BaseView):
    @classmethod
    def _to_schema(cls, clazz, actions: dict[str, str] = None) -> None:
        if not actions:
            return
        for method_name, action_name in actions.items():
            try:
                action = getattr(clazz, action_name)
            except AttributeError:
                continue
            responses = {}
            
            extracted = clazz._extract_serializer_class_with_status(method_name)
            if extracted:
                serializer_class = extracted[1]
                if issubclass(serializer_class, SerializerSchemaMixin):
                    responses |= serializer_class.to_schema(extracted[0])
            
            # noinspection PyBroadException
            try:
                action_serializer = clazz.get_serializer_class(
                    type('_', (), {'action': action_name})()
                )
                if issubclass(action_serializer, SerializerSchemaMixin):
                    responses |= action_serializer.to_schema(
                        status_by_method(method_name)
                    )
            except Exception:
                pass
            
            if issubclass(clazz, ViewSchemaMixin):
                responses |= clazz.to_schema()
            
            setattr(clazz, action_name, extend_schema(responses=responses)(action))
    
    @classmethod
    def as_view(cls, actions=None, **initkwargs):
        view = super().as_view(actions, **initkwargs)
        cls._to_schema(cls, actions)
        return csrf_exempt(view)
    
    def handle_exception(self, exception):
        return _exception_handler(exception)
