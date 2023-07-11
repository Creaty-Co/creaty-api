from __future__ import annotations

from pydantic import root_validator

from app.base.notificators.emails.base import BaseEmailNotifier
from app.base.services.email.senders.base import BaseEmailSender
from app.users.notificators.base import BaseUsersNotifier


class UsersEmailNotifier(BaseUsersNotifier, BaseEmailNotifier):
    class Notification(BaseUsersNotifier.Notification, BaseEmailNotifier.Notification):
        @root_validator(pre=True)  # noqa
        @staticmethod
        def set_email(values):
            values['email'] = values['user'].email
            return values

    def __init__(self, email_sender: BaseEmailSender):
        BaseUsersNotifier.__init__(self)
        BaseEmailNotifier.__init__(self, email_sender)
