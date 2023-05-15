from rest_framework.generics import get_object_or_404

from app.users.models import User
from app.users.serializers.password.reset import PUTUsersPasswordResetSerializer
from app.users.verification import EmailVerifier


class PasswordResetter:
    def __init__(self, verifier: EmailVerifier):
        self.verifier = verifier

    def reset(self, email: str, code, password: str) -> None:
        user = get_object_or_404(User, email=email)
        is_verified = self.verifier.check(email, code)[0]
        if not is_verified:
            raise PUTUsersPasswordResetSerializer.WARNINGS[408]
        user.set_password(password)
        user.save()
