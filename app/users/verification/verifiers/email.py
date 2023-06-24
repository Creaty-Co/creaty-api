from typing import Any

from app.base.services.cache import Cacher
from app.users.verification.code_generators.base import BaseCodeGenerator
from app.users.verification.email_senders.base import BaseEmailSender
from app.users.verification.link_generators.email.base import BaseLinkGenerator


class EmailVerifier:
    def __init__(
        self,
        email_sender: BaseEmailSender,
        cache: Cacher,
        code_generator: BaseCodeGenerator,
        link_generator: BaseLinkGenerator,
    ):
        self.email_sender = email_sender
        self.cache = cache
        self.code_generator = code_generator
        self.link_generator = link_generator

    def _update_cache(self, code, email: str, payload) -> None:
        if old_code := self.cache.get(email):
            self.cache.delete(old_code)
        self.cache.set((email, payload), code)
        self.cache.set(code, email)

    def send(self, email: str, payload=None) -> None:
        code = self.code_generator.generate()
        self._update_cache(code, email, payload)
        link = self.link_generator.generate(code, email, payload)
        self.email_sender.send(email, code, link, payload)

    def check(self, code) -> tuple[str | None, Any]:
        value = self.cache.get(code)
        if value is None:
            return None, None
        email, payload = value
        self.cache.delete(code)
        self.cache.delete(email)
        return email, payload
