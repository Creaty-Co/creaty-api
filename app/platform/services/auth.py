import hashlib
import hmac

from django.conf import settings

from app.platform.requesters.platform_api import PlatformAPIRequester
from app.users.models import User


class PlatformAuthService:
    class PlatformAuthError(Exception):
        pass

    def __init__(self, secret_key=settings.SECRET_KEY):
        self.platform_api_requester = PlatformAPIRequester()
        self.secret_key: str = secret_key

    def get_password(self, id: int) -> str:
        key = self.secret_key.encode()
        hash_ = hmac.new(key, str(id).encode(), hashlib.sha256)
        return f"A1{hash_.hexdigest()}"

    def register(self, user: User) -> None:
        self.platform_api_requester.signup(
            str(user.id), user.email, self.get_password(user.id)
        )

    def token(self, user: User) -> str:
        try:
            return self.platform_api_requester.auth(
                user.email, self.get_password(user.id)
            )
        except KeyError as exc:
            raise self.PlatformAuthError(str(exc)) from exc
