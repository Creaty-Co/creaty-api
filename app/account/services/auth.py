from django.conf import settings
from django.contrib.auth import login, logout

from app.account.models import Token, User
from app.base.logs import warning


class AuthService:
    def __init__(self):
        self.token_manager = Token.objects

    def login(self, user: User, request=None) -> Token:
        """
        :raises PermissionError: if not check_user
        """
        if not self.check_user(user):
            raise PermissionError("fail AuthService.check_user")
        token = self.token_manager.get_or_create(user=user)[0]
        if settings.SESSION_ON_LOGIN or user.is_staff:
            try:
                login(request, user)
            except ValueError as exc:
                warning(exc)
        return token

    def logout(self, user: User, request=None) -> None:
        self.token_manager.filter(user=user).delete()
        if settings.SESSION_ON_LOGIN or user.is_staff:
            try:
                logout(request)
            except ValueError as exc:
                warning(exc)

    def check_user(self, user: User) -> bool:
        return True
