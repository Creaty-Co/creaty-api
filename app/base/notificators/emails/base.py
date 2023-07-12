from __future__ import annotations

from collections.abc import Iterable

from pydantic import EmailStr, Field

from app.base.entities.base import BaseEntity
from app.base.notificators.base import BaseNotifier
from app.base.services.email.senders.base import BaseEmailSender


class BaseEmailNotifier(BaseNotifier):
    class Notification(BaseEntity):
        email: EmailStr
        context: dict = Field(default_factory=dict)

    def __init__(self, email_sender: BaseEmailSender):
        self.email_sender = email_sender

    def notify(self, notifications: Iterable[Notification]):
        for notification in notifications:
            self.email_sender.send(notification.email, **notification.context)
