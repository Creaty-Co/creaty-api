from app.bookings.models import HourlyBooking
from app.bookings.tests.views.base import BaseBookingsTest


class BookingsHourlyTest(BaseBookingsTest):
    path = '/bookings/hourly/'

    def test_post(self):
        self._test_post(HourlyBooking)
