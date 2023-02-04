from django.conf import settings

from app.users.models import User
from app.users.verification.verifiers.base import BaseVerifier


class Registerer:
    def __init__(
        self,
        verifier: BaseVerifier,
        failure_path: str = settings.VERIFICATION_REGISTER_FAILURE_PATH,
        successful_path: str = settings.VERIFICATION_REGISTER_SUCCESSFUL_PATH,
        domain: str = settings.WEB_DOMAIN,
    ):
        self.verifier = verifier
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

    def register(self, email: str, code) -> bool:
        is_verified, payload = self.verifier.check(email, code)
        if is_verified:
            self.user_manager.create(**payload)
            return True
        return False
