import urllib.parse
from abc import ABC, abstractmethod

from django.conf import settings


class BaseLinkGenerator(ABC):
    def __init__(self, domain: str = settings.WEB_DOMAIN, path: str = ''):
        self.domain = domain
        self.path = path.strip('/')

    def _generate(self, *args, **kwargs) -> str:
        args_part = '/'.join(map(str, args))
        kwargs_part = urllib.parse.urlencode(kwargs)
        path_part = f"/{self.path}" if self.path else ''
        url = f"https://{self.domain}{path_part}"
        if args_part:
            url += f"/{args_part}"
        if kwargs_part:
            url += f"?{kwargs_part}"
        return url

    @abstractmethod
    def generate(self, code, email: str, payload=None) -> str:
        raise NotImplementedError
