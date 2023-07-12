from templated_mail.mail import BaseEmailMessage

from app.base.services.email.senders.base import BaseEmailSender
from app.users.models import User


class UserEmailSender(BaseEmailSender):
    class ContextDict(BaseEmailSender.ContextDict):
        user: User

    def __init__(self, template_name, email_message_factory=BaseEmailMessage):
        super().__init__(template_name, email_message_factory)
        self.user_manager = User.objects

    def _get_user(self, email: str) -> User:
        return self.user_manager.get(email=email)

    def _create_context(self, email, **kwargs) -> ContextDict:
        return super()._create_context(email, user=self._get_user(email), **kwargs)
