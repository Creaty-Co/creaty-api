from typing import Any

from app.base.parsers import ORJSONParser
from app.base.renderers import ORJSONRenderer


class AsyncJsonConsumerMixin:
    def __init__(self):
        self.json_parser = ORJSONParser()
        self.json_renderer = ORJSONRenderer()

    async def decode_json(self, text_data) -> dict[str, Any]:
        return self.json_parser.parse(text_data)

    async def encode_json(self, content) -> str:
        return self.json_renderer.render(content).decode()
