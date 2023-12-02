from django.urls import path

from app.cal.views import CalBookView, CalScheduleView, CalTokenView

urlpatterns = [
    path('token/', CalTokenView.as_view()),
    path('trpc/public/slots.getSchedule/', CalScheduleView.as_view()),
    path('book/event/', CalBookView.as_view()),
]
