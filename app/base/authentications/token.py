from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework.authentication import TokenAuthentication as _TokenAuthentication

from app.base.authentications.utils import get_header
from app.base.exceptions import APIWarning
from app.users.models import Token


class TokenAuthentication(_TokenAuthentication):
    keyword = ''

    WARNING_401 = APIWarning("Invalid token", 401, 'invalid_token')

    def _on_auth_fail(self):
        raise self.WARNING_401

    def authenticate(self, request):
        token = get_header(request)
        if token is None or len(token.split()) > 1:
            return None
        authenticate_credentials = self.authenticate_credentials(token)
        if authenticate_credentials is None:
            request.on_auth_fail = self._on_auth_fail
        return authenticate_credentials

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.prefetch_related('user').get(key=key)
            return token.user, token
        except Token.DoesNotExist:
            return None


class TokenScheme(OpenApiAuthenticationExtension):
    target_class = 'app.base.authentications.token.TokenAuthentication'
    name = 'Token'
    match_subclasses = True
    priority = -1

    def get_security_definition(self, _):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Token-based authentication',
        }
