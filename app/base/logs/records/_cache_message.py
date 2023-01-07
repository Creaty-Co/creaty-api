import pprint
from logging import LogRecord
from typing import Optional

from django.conf import settings

__all__ = ['CacheMessageLogRecord']


class CacheMessageLogRecord(LogRecord):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__message: Optional[str] = None

    def getMessage(self) -> str:
        if self.__message:
            return self.__message
        if self.args:
            try:
                return str(self.msg) % self.args
            except TypeError:
                return str(self.msg)
        if settings.LOG_PRETTY:
            return pprint.pformat(
                self.msg, width=settings.LOG_MAX_LENGTH - 4, depth=10, sort_dicts=False
            )
        return str(self.msg)

    def setMessage(self, message: str) -> None:
        if not self.__message:
            self.__message = message
