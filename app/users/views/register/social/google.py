from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, logout
from django.urls import reverse
from drf_spectacular.utils import OpenApiResponse, extend_schema
from social_core.actions import do_auth, do_complete
from social_django.utils import load_backend, load_strategy

# noinspection PyProtectedMember
from social_django.views import _do_login

from app.base.views.base import BaseView


class UsersRegisterSocialGoogleView(BaseView):
    @extend_schema(
        responses={
            200: None,
            302: OpenApiResponse(
                description=f'redirect: {settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL}'
            ),
        }
    )
    def get(self, request):
        request.strategy = request.social_strategy = load_strategy(request)
        request.backend = load_backend(
            request.strategy, 'google-oauth2', reverse('google_complete')
        )
        return do_auth(request.backend, redirect_name=REDIRECT_FIELD_NAME)


class UsersRegisterSocialGoogleCompleteView(BaseView):
    schema = None

    def get(self, request, *args, **kwargs):
        request.strategy = request.social_strategy = load_strategy(request)
        request.backend = load_backend(
            request.strategy, 'google-oauth2', reverse('google_complete')
        )
        logout(request)
        return do_complete(
            request.backend,
            _do_login,
            user=request.user,
            redirect_name=REDIRECT_FIELD_NAME,
            request=request,
            *args,
            **kwargs,
        )
