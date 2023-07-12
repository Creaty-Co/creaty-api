from typing import Any

from app.base.services.email.senders.base import BaseEmailSender


class BaseVerificationEmailSender(BaseEmailSender):
    class ContextDict(BaseEmailSender.ContextDict):
        link: str
        code: Any

    def _create_context(
        self, email, link: str = None, code=None, payload=None
    ) -> ContextDict:
        assert link is not None
        return super()._create_context(email, link=link, code=code, payload=payload)

    def send_verification(self, email: str, link: str, code, payload=None) -> None:
        self.send(email, link=link, code=code, payload=payload)
