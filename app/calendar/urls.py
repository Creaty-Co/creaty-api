from django.urls import path

from .views import CalendarView

urlpatterns = [path('', CalendarView.as_view())]
