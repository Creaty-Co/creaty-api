from app.base.permissions.base import BasePermission
from app.users.checkers import AuthenticatedChecker


class AuthenticatedPermission(BasePermission):
    requires_authentication = True
    message = "You aren't authenticated"

    def __init__(self):
        self.checker = AuthenticatedChecker()

    def _has_permission(self, view):
        return self.checker.check(view.request.user)
