from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from rest_framework_simplejwt.tokens import RefreshToken
from social_django.strategy import DjangoStrategy

from app.base.logs import warning
from app.users.models import User
from app.users.services.auth import AuthService


class SocialStrategy(DjangoStrategy):
    def __init__(self, storage, request=None, tpl=None):
        super().__init__(storage, request, tpl)
        self.auth_service = AuthService()
        self.__user_was_created = False

    def redirect(self, url):
        if url == settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL:
            if self.__user_was_created:
                url = f"https://{settings.WEB_DOMAIN}/email-verify-success"
            token = RefreshToken.for_user(self.request.user)
            url = self.auth_service.add_token_to_url(token, url)
            response = HttpResponseRedirect(url)
            return response
        return super().redirect(url)

    def create_user(self, *args, **kwargs):
        warning(f'creating user: {kwargs}')
        try:
            kwargs['is_verified'] = True
            kwargs['has_discount'] = True
            user = super().create_user(*args, **kwargs)
            self.__user_was_created = True
            return user
        except IntegrityError as err:
            try:
                return User.objects.get(email=kwargs['email'])
            except User.DoesNotExist as exc:
                raise err from exc
