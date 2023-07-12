from __future__ import annotations

from abc import ABC
from collections.abc import Iterable

from app.base.notificators.base import BaseNotifier
from app.users.models import User


class BaseUsersNotifier(BaseNotifier, ABC):
    class Notification(BaseNotifier.Notification):
        user: User

    def __init__(self):
        self.user_manager = User.objects

    @property
    def default_users(self) -> Iterable[User]:
        return self.user_manager.all()

    def create_notification(self, user: User) -> Notification:
        return self.Notification(user=user)

    def get_users(self, users: Iterable[User] = None) -> Iterable[User]:
        return self.default_users if users is None else users

    def get_notifications(self, users: Iterable[User] = None) -> list[Notification]:
        return [self.create_notification(user) for user in self.get_users(users)]

    def notify_users(self, users: Iterable[User] = None):
        self.notify(self.get_notifications(users))
