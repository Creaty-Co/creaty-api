from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from rest_framework_simplejwt.tokens import RefreshToken
from social_django.strategy import DjangoStrategy

from app.users.models import User


class SocialStrategy(DjangoStrategy):
    def redirect(self, url):
        if url == settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL:
            token = RefreshToken.for_user(self.request.user)
            response = HttpResponseRedirect(url)
            response.set_cookie(
                key='refresh',
                value=str(token),
                domain=settings.WEB_DOMAIN,
                secure=True,
                httponly=True,
                samesite='lax',
            )
            response.set_cookie(
                key='access',
                value=token.access_token,
                domain=settings.WEB_DOMAIN,
                secure=True,
                httponly=True,
                samesite='lax',
            )
            return response
        return super().redirect(url)

    def create_user(self, *args, **kwargs):
        try:
            return super().create_user(*args, **kwargs)
        except IntegrityError as err:
            try:
                return User.objects.get(email=kwargs['email'])
            except User.DoesNotExist as exc:
                raise err from exc
