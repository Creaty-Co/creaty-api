from app.base.services.email.senders.base import BaseEmailSender
from app.users.models import User


class UserEmailSender(BaseEmailSender):
    class ContextDict(BaseEmailSender.ContextDict):
        user: User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_manager = User.objects

    def _get_user(self, email: str) -> User:
        return self.user_manager.get(email=email)

    def _create_context(self, email, **_) -> ContextDict:
        return {'user': self._get_user(email)}
