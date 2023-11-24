from django.urls import path

from app.cal.views import CalSlotsScheduleView, CalTokenView

urlpatterns = [
    path('token/', CalTokenView.as_view()),
    path('slots/schedule/', CalSlotsScheduleView.as_view()),
]
