from datetime import datetime, timedelta

import factory
from factory.django import DjangoModelFactory

from app.base.tests.fakers import fake
from app.calendar.models import CalendarEvent
from app.users.tests.factories import UserFactory


class CalendarEventFactory(DjangoModelFactory):
    start_time = factory.LazyFunction(datetime.now)
    end_time = factory.LazyFunction(
        lambda: datetime.now() + timedelta(hours=fake.random.randint(1, 3))
    )
    title = factory.Faker('sentence')
    host = factory.SubFactory(UserFactory)
    google_event_uuid = factory.Faker('uuid4')

    class Meta:
        model = CalendarEvent

    @factory.post_generation
    def guests(self, create, extracted, **_):
        if not create:
            return
        if extracted:
            for guest in extracted:
                self.guests.add(guest)
