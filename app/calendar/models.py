from django.db import models

from app.base.models.base import BaseModel
from app.calendar.managers.event import CalendarEventManager
from app.calendar.services.converters.timezone import TimezoneConverter
from app.users.models import User


class CalendarEvent(BaseModel):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    title = models.TextField()
    host = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='calendar_events_by_host'
    )
    guests = models.ManyToManyField(User, related_name='calendar_events_by_guests')
    google_event_uuid = models.UUIDField(unique=True)

    objects = CalendarEventManager()

    def save(self, **kwargs):
        timezone_converter = TimezoneConverter()
        self.start_time = timezone_converter.convert_to_utc(self.start_time)
        self.end_time = timezone_converter.convert_to_utc(self.end_time)
        super().save(**kwargs)
