from app.bookings.models import TrialBooking
from app.bookings.tests.views.base import BaseBookingsTest


class BookingsTrialTest(BaseBookingsTest):
    path = '/bookings/trial/'

    def test_post(self):
        self._test_post(TrialBooking)
