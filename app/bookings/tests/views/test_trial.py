from app.base.tests.fakers import fake
from app.base.tests.views.base import BaseViewTest
from app.bookings.models import TrialBooking
from app.mentors.tests.factories import MentorFactory


class BookingsTrialTest(BaseViewTest):
    path = '/bookings/trial/'

    def test_post(self):
        mentor = MentorFactory()
        self._test(
            'post',
            data={
                'mentor': mentor.slug,
                'name': fake.first_name(),
                'email': fake.email(),
                'description': fake.english_text(),
            },
        )
        self.assert_model(TrialBooking, {})
