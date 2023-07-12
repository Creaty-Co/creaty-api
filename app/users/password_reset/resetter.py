from app.users.models import User
from app.users.notificators.base import BaseUsersNotifier
from app.users.serializers.password.reset import PUTUsersPasswordResetSerializer
from app.users.verification import EmailVerifier


class PasswordResetter:
    def __init__(
        self,
        user_verifier: EmailVerifier,
        mentor_verifier: EmailVerifier,
        confirm_notifier: BaseUsersNotifier,
    ):
        self.user_verifier = user_verifier
        self.mentor_verifier = mentor_verifier
        self.confirm_notifier = confirm_notifier
        self.user_manager = User.objects

    def send(self, email: str) -> None:
        user = self.user_manager.get(email=email)
        verifier = self.mentor_verifier if user.is_mentor else self.user_verifier
        verifier.send(email)

    def reset(self, code, password: str) -> User:
        email = self.user_verifier.check(code)[0] or self.mentor_verifier.check(code)[0]
        if not email:
            raise PUTUsersPasswordResetSerializer.WARNINGS[408]
        user = self.user_manager.get(email=email)
        user.set_password(password)
        user.save()
        self.confirm_notifier.notify_users([user])
        return user
