from __future__ import annotations

from pydantic import root_validator

from app.base.managers.dict import DictManager
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

    def notify_users(self, users=None):
        users = [notification.user for notification in self.get_notifications(users)]
        # Patch the manager to avoid unnecessary database queries
        self.user_manager = DictManager(users, 'email')
        super().notify_users(users)
