from django.urls import path

from .views import MentorsView, MentorView

urlpatterns = [
    path('', MentorsView.as_view()),
    path('<int:id>/', MentorView.as_view()),
]
