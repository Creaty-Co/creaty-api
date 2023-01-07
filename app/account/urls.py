from django.urls import path

from .views import AccountMeView, AccountTokenView

urlpatterns = [
    path('token/', AccountTokenView.as_view()),
    path('me/', AccountMeView.as_view()),
]
