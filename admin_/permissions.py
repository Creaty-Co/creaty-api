from account.models.choices import UserType
from account.permissions import IsAuthenticatedPermission


class IsAdminPermission(IsAuthenticatedPermission):
    message = 'Вы не являетесь администратором'
    
    def _has_permission(self, request, view):
        if not super()._has_permission(request, view):
            return False
        if request.user.type >= UserType.ADMIN:
            return True
