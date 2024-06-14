import uuid
from datetime import datetime

from googleapiclient.discovery import build

from app.calendar.services.contexters.credentials import GoogleCredentialsContexter
from app.users.models import User


class GoogleCalendarEventFactory:
    def __init__(self, contexter=GoogleCredentialsContexter()):
        self.contexter = contexter
        self.google_api_version = 'v3'

    def create(
        self,
        user: User,
        summary: str,
        description: str,
        start_time: datetime,
        end_time: datetime,
        attendees: list[str],
    ) -> dict:
        with self.contexter.create_context(user.social_auth.get()) as context:
            service = build(
                serviceName='calendar',
                version=self.google_api_version,
                credentials=context.credentials,
            )
            event = {
                'summary': summary,
                'description': description,
                'start': {'dateTime': start_time.isoformat()},
                'end': {'dateTime': end_time.isoformat()},
                'reminders': {'useDefault': False},
                'attendees': [{'email': email} for email in attendees],
                'conferenceData': {
                    'createRequest': {
                        'conferenceSolutionKey': {'type': 'hangoutsMeet'},
                        'requestId': str(uuid.uuid4()),
                    }
                },
            }
            return (
                service.events()
                .insert(calendarId='primary', body=event, conferenceDataVersion=1)
                .execute()
            )
