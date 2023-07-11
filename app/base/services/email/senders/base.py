from typing import TypedDict

from templated_mail.mail import BaseEmailMessage


class BaseEmailSender:
    class ContextDict(TypedDict):
        email: str

    def __init__(
        self,
        template_name: str,
        email_message_factory: type[BaseEmailMessage] = BaseEmailMessage,
    ):
        self.template_name = template_name
        self.email_message_factory = email_message_factory

    def _create_context(self, email, **kwargs) -> ContextDict:
        return {'email': email, **kwargs}

    def send(self, email: str, **kwargs) -> None:
        email_message = self.email_message_factory(template_name=self.template_name)
        email_message.context = self._create_context(email, **kwargs)
        email_message.send([email])
