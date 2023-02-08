from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    UsersMeView,
    UsersRegisterResendView,
    UsersRegisterSocialGoogleCompleteView,
    UsersRegisterSocialGoogleView,
    UsersRegisterView,
)

urlpatterns = [
    path('register/', UsersRegisterView.as_view(), name='register'),
    path('register/resend/', UsersRegisterResendView.as_view()),
    path('register/social/google/', UsersRegisterSocialGoogleView.as_view()),
    path(
        'register/social/google/complete/',
        UsersRegisterSocialGoogleCompleteView.as_view(),
        name='google_complete',
    ),
    path('me/', UsersMeView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
