from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock

from app.base.tests.base import BaseTest
from app.base.tests.fakers import fake
from app.calendar.entites.calendar_event import CalendarEventEntity
from app.calendar.models import CalendarEvent
from app.calendar.services.factories.events.google import GoogleCalendarEventFactory
from app.users.tests.factories import UserFactory, UserSocialAuthFactory


class GoogleCalendarEventFactoryTest(BaseTest):
    @patch('app.calendar.services.factories.events.google.build')
    def test_create_event_in_google_calendar(self, mock_build):
        # Arrange
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        host = UserFactory()
        UserSocialAuthFactory(user=host)
        guests = {UserFactory(), UserFactory()}

        start_time = datetime.now(timezone.utc)
        end_time = start_time + timedelta(hours=fake.random.randint(1, 3))
        tz = fake.timezone()
        calendar_event_entity = CalendarEventEntity(
            host=host,
            title=fake.text(),
            start_time=start_time.astimezone(tz),
            end_time=end_time.astimezone(tz),
            guests=guests,
        )

        factory = GoogleCalendarEventFactory()

        # Act
        calendar_event = factory.create_event(calendar_event_entity)

        # Assert
        self.assert_model(
            CalendarEvent,
            {
                'title': calendar_event_entity.title,
                'start_time': start_time,
                'end_time': end_time,
                'google_event_uuid': calendar_event.google_event_uuid,
                'host': host.id,
                'guests': list(guests),
            },
        )
        mock_build.assert_called_once_with(
            serviceName='calendar',
            version='v3',
            credentials=mock_build.call_args[1][
                'credentials'
            ],  # Ignore specific credential instance
        )
        mock_service.events().insert.assert_called_once()
        mock_service.events().insert().execute.assert_called_once()
