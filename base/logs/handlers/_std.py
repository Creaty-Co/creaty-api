import logging
from logging import StreamHandler
from sys import stderr, stdout
from typing import Final

__all__ = ['StdHandler']


class StdHandler(StreamHandler):
    def __init__(self, err_level: int = logging.WARNING):
        super().__init__(stdout)
        self._err_level: Final[int] = err_level

    def emit(self, record):
        if record.exc_info or record.levelno >= self._err_level:
            self.stream = stderr
        super().emit(record)
        self.stream = stdout
