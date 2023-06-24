from templated_mail.mail import BaseEmailMessage


class BaseEmailSender:
    def __init__(
        self,
        template_name: str,
        email_message_factory: type[BaseEmailMessage] = BaseEmailMessage,
    ):
        self.template_name = template_name
        self.email_message_factory = email_message_factory

    def _create_context(self, email: str, code, link: str, payload) -> dict:
        return {}

    def send(self, email: str, code, link: str, payload=None) -> None:
        email_message = self.email_message_factory(template_name=self.template_name)
        email_message.context = self._create_context(email, code, link, payload)
        email_message.send([email])
