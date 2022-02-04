from templated_mail.mail import BaseEmailMessage


class EmailService:
    @staticmethod
    def _update_context(email_message: BaseEmailMessage) -> None:
        email = email_message.to[0]
        email_message.context.setdefault('email', email)
        email_message.context.setdefault('path', email_message.request.get_full_path())
    
    def send(self, email_message: BaseEmailMessage) -> None:
        self._update_context(email_message)
        email_message.send(email_message.to)
