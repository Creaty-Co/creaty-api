from account.permissions import BasePermission


class IsAdminPermission(BasePermission):
    message = 'Вы не являетесь администратором'
    
    def _has_permission(self, request, view):
        if request.user.is_staff:
            return True
