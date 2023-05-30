from typing import Any

from django.conf import settings
from templated_mail.mail import BaseEmailMessage

from app.base.services.cache import Cacher
from app.users.verification.code_generators.base import BaseCodeGenerator


class EmailVerifier:
    def __init__(
        self,
        path: str,
        template_name: str,
        cache: Cacher,
        code_generator: BaseCodeGenerator,
        domain: str = settings.API_DOMAIN,
    ):
        self.path = path.strip('/')
        self.template_name = template_name
        self.cache = cache
        self.code_generator = code_generator
        self.domain = domain

    def _generate_link(self, code) -> str:
        return f"https://{self.domain}/{self.path}/{code}"

    def _create_email_message(self, code, link: str) -> BaseEmailMessage:
        email_message = BaseEmailMessage(template_name=self.template_name)
        email_message.context = {'code': code, 'link': link}
        return email_message

    def send(self, email: str, payload=None) -> None:
        if old_code := self.cache.get(email):
            self.cache.delete(old_code)
        code = self.code_generator.generate()
        self.cache.set((email, payload), code)
        self.cache.set(code, email)
        link = self._generate_link(code)
        email_message = self._create_email_message(code, link)
        email_message.send([email])

    def check(self, code) -> tuple[str | None, Any]:
        value = self.cache.get(code)
        if value is None:
            return None, None
        email, payload = value
        self.cache.delete(code)
        self.cache.delete(email)
        return email, payload
