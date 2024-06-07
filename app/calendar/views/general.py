from datetime import datetime, timedelta

from django.conf import settings
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from rest_framework.response import Response

from app.base.views import BaseView


class CalendarView(BaseView):
    def post(self):
        user = self.request.user
        social_auth_data = user.social_auth.get(provider='google-oauth2').extra_data
        access_token = social_auth_data['access_token']
        refresh_token = social_auth_data['refresh_token']
        client_id = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
        client_secret = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
        token_uri = 'https://oauth2.googleapis.com/token'
        credentials = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri=token_uri,
            client_id=client_id,
            client_secret=client_secret,
        )
        service = build('calendar', 'v3', credentials=credentials)
        event = {
            'summary': 'Тестовая встреча',
            'location': 'Онлайн',
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
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 5},
                    {'method': 'popup', 'minutes': 5},
                ],
            },
        }
        event = service.events().insert(calendarId='primary', body=event).execute()

        return Response(data={'status': 'success', 'event': event})
