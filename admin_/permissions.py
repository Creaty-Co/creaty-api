from account.permissions import IsAuthenticatedPermission


class IsAdminPermission(IsAuthenticatedPermission):
    message = 'Вы не являетесь администратором'
    
    def _has_permission(self, request, view):
        if not super()._has_permission(request, view):
            return False
        if request.user.is_staff:
            return True
