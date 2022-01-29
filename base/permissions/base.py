from typing import final

from rest_framework.permissions import BasePermission as _BasePermission


class BasePermission(_BasePermission):
    message: str
    
    @final
    def has_permission(self, request, view):
        if self._has_permission(request, view):
            return True
        return hasattr(request, 'user') and request.user and request.user.is_superuser
    
    def _has_permission(self, request, view):
        return True
    
    @final
    def has_object_permission(self, request, view, obj):
        if self._has_object_permission(request, view, obj):
            return True
        return hasattr(request, 'user') and request.user and request.user.is_superuser
    
    def _has_object_permission(self, request, view, obj):
        return True
