from copy import copy
from typing import Any, Literal

from django.core.cache import caches


class Cacher:
    _NOT_SET = object()

    def __init__(
        self,
        scope: str,
        default: Any = None,
        timeout: int = _NOT_SET,
        cache_name: Literal['storage'] = 'default',
    ):
        self.scope = scope
        self.default = default
        self.timeout = timeout
        self.cache = caches[cache_name]

    def cache_key(self, *keys: str) -> str:
        return f'cache:{self.scope}-{"-".join(keys)}'

    def get(self, *keys: str, default=_NOT_SET):
        cache_default = self.default if default is self._NOT_SET else default
        if cache_default is self._NOT_SET:
            return self.cache.get(self.cache_key(*keys))
        return self.cache.get(self.cache_key(*keys), default=copy(cache_default))

    def set(self, value, *keys: str, timeout: int = _NOT_SET) -> None:
        cache_timeout = self.timeout if timeout is self._NOT_SET else timeout
        if cache_timeout is self._NOT_SET:
            self.cache.set(self.cache_key(*keys), value)
        else:
            self.cache.set(self.cache_key(*keys), value, timeout=cache_timeout)

    def delete(self, *keys: str) -> None:
        self.cache.delete(self.cache_key(*keys))
