import uuid

from googleapiclient.discovery import build

from app.calendar.entites.calendar_event import CalendarEventEntity
from app.calendar.services.contexters.credentials import GoogleCredentialsContexter
from app.calendar.services.factories.events.base import BaseCalendarEventFactory


class GoogleCalendarEventFactory(BaseCalendarEventFactory):
    def __init__(self):
        super().__init__()
        self.contexter = GoogleCredentialsContexter()

    def _create_event_in_google_calendar(
        self, calendar_event_entity: CalendarEventEntity
    ) -> uuid.UUID:
        host = calendar_event_entity.host
        google_event_uuid = uuid.uuid4()
        with self.contexter.create_context(host.social_auth.get()) as context:
            service = build(
                serviceName='calendar', version='v3', credentials=context.credentials
            )
            event = {
                'summary': calendar_event_entity.title,
                'description': calendar_event_entity.title,
                'start': {
                    'dateTime': calendar_event_entity.start_time.isoformat(),
                    'timeZone': 'Europe/Moscow',
                },
                'end': {
                    'dateTime': calendar_event_entity.end_time.isoformat(),
                    'timeZone': 'Europe/Moscow',
                },
                'reminders': {'useDefault': False, 'overrides': []},
                'attendees': [
                    {'email': guest.email for guest in calendar_event_entity.guests}
                ],
                'conferenceData': {
                    'createRequest': {
                        'conferenceSolutionKey': {'type': 'hangoutsMeet'},
                        'requestId': str(google_event_uuid),
                    }
                },
            }
            service.events().insert(
                calendarId='primary', body=event, conferenceDataVersion=1
            ).execute()
        return google_event_uuid

    def create_event(self, calendar_event_entity):
        google_event_uuid = self._create_event_in_google_calendar(calendar_event_entity)
        return self.calendar_event_manager.create(
            **calendar_event_entity.dict(), google_event_uuid=google_event_uuid
        )
