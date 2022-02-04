from django.urls import path

from .views import *

urlpatterns = [
    path('subscribe/', MailingsSubscribeView.as_view())
]
