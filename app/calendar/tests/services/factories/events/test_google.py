import uuid
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from app.base.tests.base import BaseTest
from app.calendar.entites.calendar_event import CalendarEventEntity
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

        calendar_event_entity = CalendarEventEntity(
            host=host,
            title="Test Event",
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=1),
            guests=guests,
        )

        factory = GoogleCalendarEventFactory()

        # Act
        event_uuid = factory._create_event_in_google_calendar(calendar_event_entity)

        # Assert
        self.assertTrue(isinstance(event_uuid, uuid.UUID))
        mock_build.assert_called_once_with(
            serviceName='calendar',
            version='v3',
            credentials=mock_build.call_args[1][
                'credentials'
            ],  # Ignore specific credential instance
        )
        mock_service.events().insert.assert_called_once()
        mock_service.events().insert().execute.assert_called_once()
