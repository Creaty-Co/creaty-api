from typing import Any, TypedDict

from app.base.services.email.senders.base import BaseEmailSender


class BaseVerificationEmailSender(BaseEmailSender):
    class ContextDict(TypedDict):
        email: str
        link: str
        code: Any

    def _create_context(
        self, email, link: str = None, code=None, payload=None
    ) -> ContextDict:
        assert link is not None
        return {'email': email, 'link': link, 'code': code}

    def send_verification(self, email: str, link: str, code, payload=None) -> None:
        self.send(email, link=link, code=code, payload=payload)
