from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework import status
from rest_framework.authentication import (
    TokenAuthentication as _TokenAuthentication
)

from account.authentications.utils import get_header
from account.models import Token
from base.exceptions import APIWarning


class TokenAuthentication(_TokenAuthentication):
    keyword = ''
    
    WARNING_401 = APIWarning(
        'Неверный токен', status.HTTP_401_UNAUTHORIZED, 'invalid_token'
    )
    
    def authenticate(self, request):
        token = get_header(request)
        if token is None or len(token.split()) > 1:
            return None
        return self.authenticate_credentials(token)
    
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.prefetch_related('user').get(key=key)
            return token.user, token
        except Token.DoesNotExist:
            raise self.WARNING_401


class TokenScheme(OpenApiAuthenticationExtension):
    target_class = 'account.authentications.token.TokenAuthentication'
    name = 'Token'
    match_subclasses = True
    priority = -1
    
    def get_security_definition(self, _):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Token-based authentication'
        }
