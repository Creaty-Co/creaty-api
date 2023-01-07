from typing import final

from rest_framework.permissions import BasePermission as _BasePermission


class BasePermission(_BasePermission):
    requires_authentication: bool = True
    message: str

    _allow_super: bool = True

    @final
    def has_permission(self, request, view):
        view.request = getattr(view, 'request', request)
        if self._has_permission(view):
            return True
        if self._allow_super and getattr(request.user, 'is_superuser', False):
            return True
        return False

    def _has_permission(self, view):
        return True

    @final
    def has_object_permission(self, request, view, obj):
        view.request = getattr(view, 'request', request)
        if self._has_object_permission(view, obj):
            return True
        if self._allow_super and getattr(request.user, 'is_superuser', False):
            return True
        return False

    def _has_object_permission(self, view, obj):
        return True
