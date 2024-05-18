from django.urls import path

from app.platform.views.token import PlatformTokenView

urlpatterns = [path('token/', PlatformTokenView.as_view())]
