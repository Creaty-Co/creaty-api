from django.urls import path

from .views import *

urlpatterns = [
    path('main/', PagesMainView.as_view()),
    path('personal/<str:shortcut>/', PagesPersonalView.as_view())
]
