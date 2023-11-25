from django.conf import settings

from app.base.requesters.base import BaseRequester


class CalAPIRequester(BaseRequester):
    class CalAPIError(Exception):
        pass

    def __init__(self, **kwargs):
        kwargs['default_kwargs'] = kwargs.get('default_kwargs', {}) | {
            'allow_redirects': False
        }
        base_url = f"http://{settings.CAL_API_DOMAIN}/api"
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
        return self.request('get', 'auth/csrf').json()['csrfToken']

    def auth(self, email: str, password: str, csrf: str = None) -> str:
        csrf = csrf or self.csrf()
        return self.request(
            'post',
            'auth/callback/credentials',
            data={'email': email, 'password': password, 'csrfToken': csrf},
        ).cookies['next-auth.session-token']

    def get_schedule(self, input_str: str) -> dict:
        return self.request(
            'get', 'trpc/public/slots.getSchedule', query_params={'input': input_str}
        ).json()

    def post_book_event(self, data: dict) -> dict:
        return self.request('post', 'book/event', data=data).json()
