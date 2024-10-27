from django.db import models

from app.users.models import User


class CalendarEventManager(models.Manager):
    def create(self, **kwargs):
        from app.calendar.models import CalendarEvent

        guests: set[User] = set(kwargs.pop('guests', set()))
        calendar_event: CalendarEvent = super().create(**kwargs)
        calendar_event.guests.set(guests)
        return calendar_event
