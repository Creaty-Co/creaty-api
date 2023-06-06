from app.base.tests.fakers import fake
from app.base.tests.views.base import BaseViewTest
from app.bookings.models import HourlyBooking
from app.mentors.tests.factories import PackageFactory


class BookingsHourlyTest(BaseViewTest):
    path = '/bookings/hourly/'

    def test_post(self):
        package = PackageFactory()
        mentor = package.mentor
        self._test(
            'post',
            data={
                'mentor': mentor.slug,
                'name': fake.first_name(),
                'email': fake.email(),
                'description': fake.english_text(),
                'package': package.id,
            },
        )
        self.assert_model(HourlyBooking, {})
