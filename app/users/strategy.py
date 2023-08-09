from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from rest_framework_simplejwt.tokens import RefreshToken
from social_django.strategy import DjangoStrategy

from app.users.models import User
from app.users.notificators.email import UsersEmailNotifier
from app.users.services.auth import AuthService
from app.users.services.email.senders.user import UserEmailSender


class SocialStrategy(DjangoStrategy):
    def __init__(self, storage, request=None, tpl=None):
        super().__init__(storage, request, tpl)
        self.auth_service = AuthService()
        self.confirm_notifier = UsersEmailNotifier(
            email_sender=UserEmailSender(template_name='email/account-verified.html')
        )
        self.__user_was_created = False

    def redirect(self, url):
        if url == settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL:
            user = self.request.user
            if self.__user_was_created:
                self.confirm_notifier.notify_users([user])
                url = f"https://{settings.WEB_DOMAIN}/email-verify-success"
            token = RefreshToken.for_user(user)
            url = self.auth_service.add_token_to_url(token, url)
            response = HttpResponseRedirect(url)
            return response
        return super().redirect(url)

    def create_user(self, *args, **kwargs):
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
