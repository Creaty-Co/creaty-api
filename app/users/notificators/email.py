from __future__ import annotations

from collections.abc import Iterable

from pydantic import model_validator  # noqa

from app.base.notificators.emails.base import BaseEmailNotifier
from app.base.services.email.senders.base import BaseEmailSender
from app.users.notificators.base import BaseUsersNotifier


class UsersEmailNotifier(BaseUsersNotifier, BaseEmailNotifier):
    class Notification(BaseUsersNotifier.Notification, BaseEmailNotifier.Notification):
        @model_validator(mode='before')  # noqa
        @staticmethod
        def set_email(values):
            values['email'] = values['user'].email
            return values

    def __init__(self, email_sender: BaseEmailSender):
        BaseUsersNotifier.__init__(self)
        BaseEmailNotifier.__init__(self, email_sender)

    def notify(self, notifications: Iterable[Notification]):
        for notification in notifications:
            notification.context.setdefault('user', notification.user)
        BaseEmailNotifier.notify(self, notifications)

    def create_notification(self, user) -> Notification:
        return self.Notification(user=user, email=user.email)
