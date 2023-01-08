from django.urls import path

from app.base.consumers import EchoConsumer
from app.base.views import BaseFrontErrorView, EchoView
from app.base.views.status import StatusView

urlpatterns = [
    path('echo/', EchoView.as_view()),
    path('front/error/', BaseFrontErrorView.as_view()),
    path('status/', StatusView.as_view()),
]

ws_urlpatterns = [
    path('ws/echo/', EchoConsumer.as_asgi()),
]
