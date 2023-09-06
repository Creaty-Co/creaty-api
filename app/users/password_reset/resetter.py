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

    def _get_verifier(self, user: User) -> EmailVerifier:
        return (
            self.mentor_verifier
            if user.to_mentor is not None and not user.to_mentor.is_registered
            else self.user_verifier
        )

    def _send(self, email: str, verifier) -> None:
        verifier.send(email)

    def send(self, email: str) -> None:
        user = self.user_manager.get(email=email)
        self._send(email, self._get_verifier(user))

    def send_to_user(self, email: str) -> None:
        self._send(email, self.user_verifier)

    def send_to_mentor(self, email: str) -> None:
        user = self.user_manager.get(email=email)
        assert user.to_mentor is not None
        self._send(email, self.mentor_verifier)

    def reset(self, code, password: str) -> User:
        email = self.user_verifier.check(code)[0] or self.mentor_verifier.check(code)[0]
        if not email:
            raise PUTUsersPasswordResetSerializer.WARNINGS[408]
        user = self.user_manager.get(email=email)
        will_notify = True
        if self._get_verifier(user) is self.mentor_verifier:
            will_notify = False
        user.set_password(password)
        user.save()
        if will_notify:
            self.confirm_notifier.notify_users([user])
        return user
