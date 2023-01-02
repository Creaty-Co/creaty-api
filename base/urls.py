from django.urls import path

from base.views import BaseFrontErrorView, EchoView

urlpatterns = [
    path('echo/', EchoView.as_view()),
    path('front/error/', BaseFrontErrorView.as_view()),
]
