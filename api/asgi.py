import os

import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

django.setup()

from app.base.middlewares.ws_log import WsLogMiddleware  # noqa:E402
from app.base.middlewares.ws_token_auth import TokenAuthMiddleware  # noqa:E402
from app.base.urls import ws_urlpatterns as base_ws_urls  # noqa:E402

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': TokenAuthMiddleware(WsLogMiddleware(URLRouter(base_ws_urls))),
    }
)
