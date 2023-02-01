from app.users.permissions import AuthenticatedPermission


class AdminPermission(AuthenticatedPermission):
    message = "You aren't an admin"

    def _has_permission(self, view):
        if not super()._has_permission(view):
            return False
        if view.request.user.is_staff:
            return True
