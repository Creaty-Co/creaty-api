from django.urls import path

from .views import *

urlpatterns = [
    path('<str:shortcut>/', PageView.as_view())
]
