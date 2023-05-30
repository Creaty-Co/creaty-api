from app.users.models import User
from app.users.serializers.password.reset import PUTUsersPasswordResetSerializer
from app.users.verification import EmailVerifier


class PasswordResetter:
    def __init__(self, verifier: EmailVerifier):
        self.verifier = verifier
        self.user_manager = User.objects

    def reset(self, code, password: str) -> User:
        email = self.verifier.check(code)[0]
        if not email:
            raise PUTUsersPasswordResetSerializer.WARNINGS[408]
        user = self.user_manager.get(email=email)
        user.set_password(password)
        user.save()
        return user
