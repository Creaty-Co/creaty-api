from abc import ABC, abstractmethod
from typing import TypedDict

from templated_mail.mail import BaseEmailMessage


class BaseEmailSender(ABC):
    class ContextDict(TypedDict):
        pass

    def __init__(
        self,
        template_name: str,
        email_message_factory: type[BaseEmailMessage] = BaseEmailMessage,
    ):
        self.template_name = template_name
        self.email_message_factory = email_message_factory

    @abstractmethod
    def _create_context(self, email, **kwargs) -> ContextDict:
        raise NotImplementedError

    def send(self, email: str, **kwargs) -> None:
        email_message = self.email_message_factory(template_name=self.template_name)
        email_message.context = self._create_context(email, **kwargs)
        email_message.send([email])
