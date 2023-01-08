from app.account.enums.users import UserType
from app.account.permissions import AuthenticatedPermission


class AdminPermission(AuthenticatedPermission):
    message = 'Вы не являетесь администратором'

    def _has_permission(self, view):
        if not super()._has_permission(view):
            return False
        if view.request.user.type >= UserType.ADMIN:
            return True
