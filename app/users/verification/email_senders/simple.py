from app.users.verification.email_senders.base import BaseEmailSender


class SimpleEmailSender(BaseEmailSender):
    def _create_context(self, email: str, code, link: str, payload):
        return {'email': email, 'link': link}
