import hashlib
import hmac

from django.conf import settings

from app.calcom.requesters.cal_api import CalAPIRequester
from app.users.models import User


class CalAuthService:
    class CalAuthError(Exception):
        pass

    def __init__(self, secret_key=settings.SECRET_KEY):
        self.cal_api_requester = CalAPIRequester()
        self.secret_key = secret_key

    def get_password(self, id: int) -> str:
        key = self.secret_key.encode()
        hash_ = hmac.new(key, str(id).encode(), hashlib.sha256)
        return hash_.hexdigest()

    def register(self, user: User) -> None:
        self.cal_api_requester.signup(
            str(user.id), user.email, self.get_password(user.id)
        )

    def token(self, user: User) -> str:
        try:
            return self.cal_api_requester.auth(user.email, self.get_password(user.id))
        except KeyError as exc:
            raise self.CalAuthError(str(exc)) from exc
