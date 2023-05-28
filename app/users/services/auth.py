from rest_framework_simplejwt.tokens import RefreshToken

from app.base.utils.common import add_query_params


class AuthService:
    def add_token_to_url(self, token: RefreshToken, url: str) -> str:
        return add_query_params(url, refresh=str(token), access=token.access_token)
