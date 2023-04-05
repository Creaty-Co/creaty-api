from datetime import timedelta

from django.conf import settings
from django.http import HttpResponseRedirect

from app.users.verification import EmailVerifier


class PasswordResetter:
    def __init__(
        self,
        verifier: EmailVerifier,
        failure_path: str = settings.VERIFICATION_PASSWORD_RESET_FAILURE_PATH,
        successful_path: str = settings.VERIFICATION_PASSWORD_RESET_SUCCESSFUL_PATH,
        domain: str = settings.WEB_DOMAIN,
    ):
        self.verifier = verifier
        self.failure_path = failure_path
        self.successful_path = successful_path
        self.domain = domain

    @property
    def failure_url(self) -> str:
        return f"https://{self.domain}/{self.failure_path.strip('/')}"

    @property
    def successful_url(self) -> str:
        return f"https://{self.domain}/{self.successful_path.strip('/')}"

    def redirect(self, email: str, session_id) -> HttpResponseRedirect:
        if self.verifier.check(email, session_id):
            response = HttpResponseRedirect(self.successful_url)
            response.set_cookie(
                key='session_id',
                value=session_id,
                max_age=timedelta(hours=1),
                domain=settings.ROOT_DOMAIN,
                secure=True,
                httponly=True,
                samesite='Lax',
            )
            return response
        return HttpResponseRedirect(self.failure_url)

    def reset(self, email, session_id) -> None:
        # TODO
        # is_verified, payload = self.verifier.check(email, code)
        # if is_verified:
        #     self.user_manager.create(**payload)
        #     return True
        # return False
        pass
