from django.urls import path

from .views import MentorsView, MentorView

urlpatterns = [
    path('', MentorsView.as_view()),
    path('<str:slug>/', MentorView.as_view()),
]
