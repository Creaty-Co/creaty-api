from django.urls import path

from app.bookings.views.hourly import BookingsHourlyView
from app.bookings.views.package import BookingsPackageView
from app.bookings.views.slots.trial import BookingsSlotsTrialView
from app.bookings.views.trial import BookingsTrialView

urlpatterns = [
    path('trial/', BookingsTrialView.as_view()),
    path('hourly/', BookingsHourlyView.as_view()),
    path('package/', BookingsPackageView.as_view()),
    path('slots/trial/', BookingsSlotsTrialView.as_view()),
]
