from django.core import mail

from app.base.tests.fakers import fake
from app.base.tests.views.base import BaseViewTest
from app.bookings.models import AbstractBooking
from app.mentors.models import Package
from app.mentors.tests.factories import MentorFactory
from app.users.tests.factories import GroupFactory, UserFactory


class BaseBookingsTest(BaseViewTest):
    def _test_post(self, model: type[AbstractBooking], package: Package = None):
        operator = UserFactory()
        operator.groups.add(GroupFactory(name='operator'))
        mentor = MentorFactory()
        email = fake.email()
        self._test(
            'post',
            data={
                'mentor': mentor.slug,
                'name': fake.first_name(),
                'email': email,
                'description': fake.english_text(),
                'package': package.id if package else None,
            },
        )
        self.assert_model(model, {'package': package.id} if package else {})
        self.assert_equal(
            {
                lambda message: self.assert_equal(message.to, [email]),
                lambda message: self.assert_equal(message.to, [operator.email]),
            },
            set(mail.outbox),
        )
