from app.users.services.email.senders.user import UserEmailSender
from app.users.verification.email_senders.base import BaseVerificationEmailSender


class UserVerificationEmailSender(BaseVerificationEmailSender, UserEmailSender):
    class ContextDict(
        BaseVerificationEmailSender.ContextDict, UserEmailSender.ContextDict
    ):
        pass

    def __init__(self, *args, **kwargs):
        BaseVerificationEmailSender.__init__(self, *args, **kwargs)
        UserEmailSender.__init__(self, *args, **kwargs)

    def _create_context(self, email, link=None, code=None, payload=None):
        return BaseVerificationEmailSender._create_context(
            self, email, link, code, payload
        ) | UserEmailSender._create_context(self, email)
