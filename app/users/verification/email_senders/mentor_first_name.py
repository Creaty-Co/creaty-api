from app.users.models import User
from app.users.verification.email_senders.base import BaseEmailSender


class UserEmailSender(BaseEmailSender):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_manager = User.objects

    def _create_context(self, email: str, code, link: str, payload):
        user = self.user_manager.get(email=email)
        return {'email': email, 'link': link, 'user': user}
