from datetime import timedelta

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
            for key, value in ('refresh', str(token)), ('access', token.access_token):
                response.set_cookie(
                    key=key,
                    value=value,
                    max_age=timedelta(hours=1),
                    domain=settings.ROOT_DOMAIN,
                    secure=True,
                    samesite='Lax',
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
