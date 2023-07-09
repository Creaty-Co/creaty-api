from django.conf import settings

from app.base.services.email.senders.base import BaseEmailSender
from app.users.models import User
from app.users.verification import EmailVerifier


class Registerer:
    class InvalidCodeError(Exception):
        pass

    def __init__(
        self,
        verifier: EmailVerifier,
        confirm_email_sender: BaseEmailSender,
        failure_path: str = settings.VERIFICATION_REGISTER_FAILURE_PATH,
        successful_path: str = settings.VERIFICATION_REGISTER_SUCCESSFUL_PATH,
        domain: str = settings.WEB_DOMAIN,
    ):
        self.verifier = verifier
        self.confirm_email_sender = confirm_email_sender
        self.failure_path = failure_path
        self.successful_path = successful_path
        self.domain = domain
        self.user_manager = User.objects

    @property
    def failure_url(self) -> str:
        return f"https://{self.domain}/{self.failure_path.strip('/')}"

    @property
    def successful_url(self) -> str:
        return f"https://{self.domain}/{self.successful_path.strip('/')}"

    def register(self, code) -> User:
        email = self.verifier.check(code)[0]
        if email:
            user = self.user_manager.get(email=email)
            user.has_discount = True
            user.is_verified = True
            user.save()
            self.confirm_email_sender.send(email)
            return user
        raise self.InvalidCodeError
