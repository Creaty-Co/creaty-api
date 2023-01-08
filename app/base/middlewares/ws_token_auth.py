from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from app.account.models import User
from app.base.exceptions import ClientError


@database_sync_to_async
def get_user(key):
    try:
        return User.objects.get(auth_token__key=key)
    except User.DoesNotExist:
        return None


class TokenAuthMiddleware(BaseMiddleware):
    def get_token(self, scope):
        try:
            query_params = parse_qs(scope['query_string'].decode())
            scope['query_params'] = {k: v[0] for k, v in query_params.items()}
            return scope['query_params']['token']
        except UnicodeError:
            raise ClientError("Неверная кодировка параметра запроса с токеном")
        except KeyError:
            return None

    async def __call__(self, scope, receive, send):
        token = self.get_token(scope)
        scope['user'] = await get_user(token)
        return await super().__call__(scope, receive, send)
