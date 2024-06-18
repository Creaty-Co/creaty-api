from rest_framework.response import Response

from app.base.views import BaseView
from app.calendar.factories.event import GoogleCalendarEventFactory


class CalendarView(BaseView):
    def post(self):
        user = self.request.user
        google_calendar_event_factory = GoogleCalendarEventFactory()
        event = google_calendar_event_factory.create(user)
        return Response(data={'status': 'success', 'event': event})
