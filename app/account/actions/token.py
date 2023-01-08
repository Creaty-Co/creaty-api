from django.contrib.auth import authenticate
from rest_framework.request import Request

from app.account.models import User
from app.account.services.auth import AuthService
from app.base.actions.base import BaseAction
from app.base.entities.base import BaseEntity


class POST_UsersTokenAction(BaseAction):
    class InEntity(BaseEntity):
        email: str
        password: str
        request: Request

    class OutEntity(BaseEntity):
        token: str

    def __init__(self):
        self.auth_service = AuthService()

    def run(self, data: InEntity) -> OutEntity:
        """
        :raises PermissionError: if username doesn't exists or password is invalid or
            not auth_service.check_user
        """
        user = authenticate(
            request=data.request, email=data.email, password=data.password
        )
        if user is None:
            raise PermissionError
        self.auth_service.check_user(user)
        return self.OutEntity(token=self.auth_service.login(user, data.request).key)


class DELETE_UsersTokenAction(BaseAction):
    class InEntity(BaseEntity):
        user: User
        request: Request

    def __init__(self):
        self.auth_service = AuthService()

    def run(self, data: InEntity) -> None:
        self.auth_service.logout(data.user, data.request)
