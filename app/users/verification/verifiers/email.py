import urllib.parse
from typing import Any

from django.conf import settings
from django.urls import reverse
from templated_mail.mail import BaseEmailMessage

from app.base.services.cache import Cacher
from app.users.verification.code_generators.base import BaseCodeGenerator


class EmailVerifier:
    class ResendEmailNotFoundException(Exception):
        pass

    def __init__(
        self,
        view_name: str,
        template_name: str,
        cache: Cacher,
        code_generator: BaseCodeGenerator,
        domain: str = settings.API_DOMAIN,
    ):
        self.view_name = view_name
        self.template_name = template_name
        self.cache = cache
        self.code_generator = code_generator
        self.domain = domain

    def _generate_link(self, email: str, code) -> str:
        path = f"/{reverse(self.view_name).strip('/')}/"
        query_string = urllib.parse.urlencode({'email': email, 'code': code})
        return f"https://{self.domain}{path}?{query_string}"

    def _create_email_message(self, code, link: str) -> BaseEmailMessage:
        email_message = BaseEmailMessage(template_name=self.template_name)
        email_message.context = {'code': code, 'link': link}
        return email_message

    def send(self, email: str, payload=None) -> None:
        code = self.code_generator.generate()
        self.cache.set((code, payload), email)
        link = self._generate_link(email, code)
        email_message = self._create_email_message(code, link)
        email_message.send([email])

    def resend(self, email: str) -> None:
        try:
            _, payload = self.cache.get(email)
        except TypeError as exc:
            raise self.ResendEmailNotFoundException from exc
        new_code = self.code_generator.generate()
        self.cache.set((new_code, payload), email)
        link = self._generate_link(email, new_code)
        email_message = self._create_email_message(new_code, link)
        email_message.send([email])

    def check(self, email: str, code) -> tuple[bool, Any]:
        value = self.cache.get(email)
        if value is None:
            return False, None
        cached_code, payload = value
        if self.code_generator.is_equal(cached_code, code):
            self.cache.delete(email)
            return True, payload
        return False, None
