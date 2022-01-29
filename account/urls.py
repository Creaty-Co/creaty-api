from django.urls import path

from .views import *

urlpatterns = [
    path('token/', AccountsTokenView.as_view()),
    path('me/', AccountsMeView.as_view())
]
