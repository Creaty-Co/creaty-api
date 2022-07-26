from __future__ import annotations

from django.conf import settings
from django.contrib.auth import login, logout

from account.models import User, Token
from base.logs import debug


class AuthService:
    def __init__(self, request, user=None):
        self.request = request
        self.user = user or request.user

    def login(self) -> str:
        token = Token.objects.get_or_create(user=self.user)[0].key
        if settings.SESSION_ON_LOGIN:
            try:
                login(self.request, self.user)
            except ValueError as e:
                debug(e)
        return token

    def logout(self) -> None:
        self.delete_token(self.user)
        if settings.SESSION_ON_LOGIN:
            logout(self.request)

    @classmethod
    def user_by_token(cls, token: str) -> User | None:
        return User.objects.filter(auth_token__key=token).first()

    @classmethod
    def delete_token(cls, user) -> None:
        Token.objects.filter(user=user).delete()
