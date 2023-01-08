from channels.middleware import BaseMiddleware

from app.base.exceptions.handler import exception_handler
from app.base.logs import info


class WsLogMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        info(f"{scope = }")
        try:
            return await super().__call__(scope, receive, send)
        except Exception as error:
            exception_handler(error)
