from django.urls import path

from base.views import *

urlpatterns = [
    path('echo/', EchoView.as_view())
]
