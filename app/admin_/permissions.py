from app.users.enums.roles import UserRole
from app.users.permissions import AuthenticatedPermission


class AdminPermission(AuthenticatedPermission):
    message = 'Вы не являетесь администратором'

    def _has_permission(self, view):
        if not super()._has_permission(view):
            return False
        if view.request.user.role >= UserRole.ADMIN:
            return True
