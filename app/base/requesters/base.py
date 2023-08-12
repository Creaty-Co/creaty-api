from urllib.parse import urlencode, urljoin, urlparse, urlunparse

import requests

from app.base.constants.immutables import im_dict


class BaseRequester:
    def __init__(
        self,
        base_url: str,
        session_factory=requests.Session,
        default_kwargs: dict = im_dict,
    ):
        self.base_url = base_url
        self.session_factory = session_factory
        self.default_kwargs = default_kwargs
        self._session = None

    @property
    def session(self):
        self._session = self._session or self.session_factory()
        return self._session

    def reset_session(self) -> None:
        self._session = None

    def get_url(self, path: str, query_params: dict, hash_: str) -> str:
        parsed_base_url = urlparse(self.base_url)
        full_path = urljoin(parsed_base_url.path.rstrip('/') + '/', path.rstrip('/'))
        url_components = (
            parsed_base_url.scheme,
            parsed_base_url.netloc,
            full_path,
            '',
            urlencode(query_params),
            hash_,
        )
        return urlunparse(url_components)

    def request(
        self,
        method: str,
        path: str = '',
        query_params: str = None,
        hash_: str = '',
        headers: dict = im_dict,
        data: dict = im_dict,
        **kwargs,
    ):
        url = self.get_url(path, query_params or {}, hash_)
        kwargs = self.default_kwargs | kwargs | {'headers': headers} | {'data': data}
        return getattr(self.session, method)(url, **kwargs)
