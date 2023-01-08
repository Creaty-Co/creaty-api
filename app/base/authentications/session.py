from django.conf import settings
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework.authentication import (
    SessionAuthentication as _SessionAuthentication,
)


class SessionAuthentication(_SessionAuthentication):
    def enforce_csrf(self, request):
        pass


class SessionScheme(OpenApiAuthenticationExtension):
    target_class = 'app.base.authentications.session.SessionAuthentication'
    name = 'Cookie'
    priority = -2

    def get_security_definition(self, auto_schema):
        return {'type': 'apiKey', 'in': 'cookie', 'name': settings.SESSION_COOKIE_NAME}
