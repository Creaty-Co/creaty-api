from templated_mail.mail import BaseEmailMessage

from app.users.services.email.senders.user import UserEmailSender
from app.users.verification.email_senders.base import BaseVerificationEmailSender


class UserVerificationEmailSender(BaseVerificationEmailSender, UserEmailSender):
    class ContextDict(
        BaseVerificationEmailSender.ContextDict, UserEmailSender.ContextDict
    ):
        pass

    def __init__(self, template_name, email_message_factory=BaseEmailMessage):
        BaseVerificationEmailSender.__init__(self, template_name, email_message_factory)
        UserEmailSender.__init__(self, template_name, email_message_factory)

    def _create_context(self, email, link=None, code=None, payload=None):
        return BaseVerificationEmailSender._create_context(
            self, email, link, code, payload
        ) | UserEmailSender._create_context(self, email)
