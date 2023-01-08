from logging import Formatter
from textwrap import wrap
from typing import Final

from django.conf import settings

from app.base.logs.records import CacheMessageLogRecord

__all__ = ['WrapFormatter']


def _tab(text: str) -> str:
    if text.endswith('\n'):
        return '\t' + text.replace('\n', '\n\t')[:-1]
    return '\t' + text.replace('\n', '\n\t')


def _wrap(text: str, max_length: int) -> str:
    wrapped_text_list = []
    if not text.startswith('\n'):
        text = '\n' + text
    for line in text.split('\n'):
        wrapped_text_list.extend(wrap(line, max_length))
    if text.startswith('\n'):
        return '\n' + '\n'.join(wrapped_text_list)
    return '\n'.join(wrapped_text_list)


class WrapFormatter(Formatter):
    def __init__(self, *args, max_length: int = settings.LOG_MAX_LENGTH, **kwargs):
        super().__init__(*args, **kwargs)
        self._max_length: Final[int] = max_length

    def format(self, record: CacheMessageLogRecord):
        formatted = super().format(record)
        if settings.LOG_PRETTY and (
            '\n' in record.message or len(formatted) > self._max_length
        ):
            old_message = record.message
            record.setMessage(_tab(_wrap(record.message, self._max_length)))
            formatted = super().format(record)
            record.message = old_message
        return formatted
