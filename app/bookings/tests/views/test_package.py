from app.bookings.models import PackageBooking
from app.bookings.tests.views.base import BaseBookingsTest
from app.mentors.tests.factories import PackageFactory


class BookingsPackageTest(BaseBookingsTest):
    path = '/bookings/package/'

    def test_post(self):
        package = PackageFactory()
        self._test_post(PackageBooking, package)
