import uuid
from datetime import datetime, timedelta

from googleapiclient.discovery import build
from rest_framework.response import Response

from app.base.views import BaseView
from app.calendar.services.contexters.credentials import GoogleCredentialsContexter


class CalendarView(BaseView):
    def post(self):
        user = self.request.user
        contexter = GoogleCredentialsContexter()
        with contexter.create_context(user.social_auth.get()) as context:
            service = build(
                serviceName='calendar', version='v3', credentials=context.credentials
            )
            event = {
                'summary': 'Тестовая встреча',
                'description': 'Тестовая встреча, созданная через Google Calendar API',
                'start': {
                    'dateTime': (
                        datetime.now() + timedelta(hours=3, minutes=10)
                    ).isoformat(),
                    'timeZone': 'Europe/Moscow',
                },
                'end': {
                    'dateTime': (
                        datetime.now() + timedelta(hours=3, minutes=20)
                    ).isoformat(),
                    'timeZone': 'Europe/Moscow',
                },
                'reminders': {'useDefault': False, 'overrides': []},
                'attendees': [{'email': 'envy42125@gmail.com'}],
                'conferenceData': {
                    'createRequest': {
                        'conferenceSolutionKey': {'type': 'hangoutsMeet'},
                        'requestId': str(uuid.uuid4()),
                    }
                },
            }
            event = (
                service.events()
                .insert(calendarId='primary', body=event, conferenceDataVersion=1)
                .execute()
            )
        return Response(data={'status': 'success', 'event': event})
