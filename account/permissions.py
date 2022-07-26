from base.permissions.base import BasePermission


class IsAuthenticatedPermission(BasePermission):
    message = 'Вы не авторизованы'

    def _has_permission(self, request, view):
        return (
            hasattr(request, 'user') and request.user and request.user.is_authenticated
        )
