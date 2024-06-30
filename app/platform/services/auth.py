import hashlib
import hmac

from django.conf import settings
from rest_framework.response import Response

from app.platform.requesters.platform_api import PlatformAPIRequester
from app.users.models import User


class PlatformAuthService:
    class PlatformAuthError(Exception):
        pass

    def __init__(
        self, secret_key=settings.SECRET_KEY, cookie_domain=f"{settings.ROOT_DOMAIN}"
    ):
        self.platform_api_requester = PlatformAPIRequester()
        self.secret_key: str = secret_key
        self.cookie_domain: str = cookie_domain

    def get_password(self, id: int) -> str:
        key = self.secret_key.encode()
        hash_ = hmac.new(key, str(id).encode(), hashlib.sha256)
        return f"A1{hash_.hexdigest()}"

    def register(self, user: User) -> None:
        username = mentor.slug if (mentor := user.to_mentor) else str(user.id)
        self.platform_api_requester.signup(
            user.id, username, user.email, self.get_password(user.id)
        )

    def token(self, user: User) -> str:
        try:
            return self.platform_api_requester.auth(
                user.email, self.get_password(user.id)
            )
        except KeyError as exc:
            raise self.PlatformAuthError(str(exc)) from exc

    def set_cookie(self, token: str, response: Response = Response()) -> Response:
        response.set_cookie(
            'next-auth.session-token',
            token,
            # domain=self.cookie_domain,
            httponly=True,
            samesite='Lax',
        )
        return response
