# source:
#   https://github.com/brianjbuck/drf_orjson_renderer/blob/master/drf_orjson_renderer
#   /parsers.py

# Didn't pip install because https://github.com/brianjbuck/drf_orjson_renderer/issues/20

from typing import IO, Any, Optional

import orjson
from django.conf import settings
from rest_framework.exceptions import ParseError
from rest_framework.parsers import BaseParser

__all__ = ['ORJSONParser']


class ORJSONParser(BaseParser):
    """
    Parses JSON-serialized data by orjson parser.
    """

    media_type: str = "application/json"

    def parse(
        self,
        data_or_stram: str | bytes | bytearray | memoryview | IO,
        media_type: Optional[Any] = None,
        parser_context: Any = None,
    ) -> Any:
        """
        De-serializes JSON strings to Python objects.
        :param data_or_stram: A byte data or stream-like object representing the body
        of the request.
        :param media_type: If provided, this is the media type of the incoming
        request content specified in the `Content-Type` HTTP header.
        :param parser_context: If supplied, this argument will be a dictionary
        containing any additional context that may be required to parse
        the request content.
        By default this will include the following keys: view, request, args, kwargs.
        :return: Python native instance of the JSON string.
        """
        parser_context = parser_context or {}
        encoding: str = parser_context.get('encoding', settings.DEFAULT_CHARSET)
        if hasattr(data_or_stram, 'read'):
            data = data_or_stram.read()
        else:
            data = data_or_stram
        if not isinstance(data, str):
            data = data.decode(encoding)
        try:
            return orjson.loads(data)
        except orjson.JSONDecodeError as exc:
            raise ParseError(f"JSON parse error - {exc.args[0]}")
