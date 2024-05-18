from django.conf import settings

from app.base.logs import debug
from app.base.requesters.base import BaseRequester


class PlatformAPIRequester(BaseRequester):
    class CalAPIError(Exception):
        pass

    def __init__(self, base_url: str = settings.PLATFORM_API_URL, **kwargs):
        headers = {'Host': settings.DOMAIN} | kwargs.get('headers', {})
        kwargs['default_kwargs'] = kwargs.get('default_kwargs', {}) | {
            'allow_redirects': False,
            'headers': headers,
        }
        super().__init__(base_url=base_url, **kwargs)

    def signup(self, username: str, email: str, password: str) -> None:
        message = self.request(
            'post',
            'auth/signup',
            data={'username': username, 'email': email, 'password': password},
        ).json()['message']
        if message != 'Created user':
            raise self.CalAPIError(message)

    def csrf(self) -> str:
        response = self.request('get', 'auth/csrf')
        debug(response)
        return response.json()['csrfToken']

    def auth(self, email: str, password: str, csrf: str = None) -> str:
        csrf = csrf or self.csrf()
        return self.request(
            'post',
            'auth/callback/credentials',
            data={'email': email, 'password': password, 'csrfToken': csrf},
        ).cookies['next-auth.session-token']
