from django.core.cache import cache


class BaseCacheService:
    SCOPE: str

    _NOT_SET = object()
    DEFAULT = None
    TIMEOUT = _NOT_SET

    def cache_key(self, *keys: str) -> str:
        return f'cache:{self.SCOPE}-{"-".join(keys)}'

    def get(self, *keys: str, default=_NOT_SET):
        cache_default = self.DEFAULT if default is self._NOT_SET else default
        if cache_default is self._NOT_SET:
            return cache.get(self.cache_key(*keys))
        return cache.get(self.cache_key(*keys), default=cache_default)

    def set(self, value, *keys: str, timeout: int = _NOT_SET) -> None:
        cache_timeout = self.TIMEOUT if timeout is self._NOT_SET else timeout
        if cache_timeout is self._NOT_SET:
            cache.set(self.cache_key(*keys), value)
        else:
            cache.set(self.cache_key(*keys), value, timeout=cache_timeout)

    def delete(self, *keys: str) -> None:
        cache.delete(self.cache_key(*keys))
