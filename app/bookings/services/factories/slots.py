from datetime import datetime, date, timezone, timedelta

from django.db import models

from app.bookings.entites.slot import SlotEntity
from app.calendar.models import CalendarEvent
from app.users.models import User


class BookingSlotsFactory:
    def __init__(self):
        self.calendar_event_manager = CalendarEvent.objects

    def _get_events_for_day(
        self, user: User, start_of_day: datetime
    ) -> models.QuerySet:
        start_of_day = start_of_day.astimezone(timezone.utc)
        end_of_day = start_of_day + timedelta(days=1)
        return CalendarEvent.objects.filter(
            models.Q(start_time__lte=end_of_day) & models.Q(end_time__gte=start_of_day),
            models.Q(host=user) | models.Q(guests=user),
        )

    def create_slots_for_day(
        self, user: User, day: date, tz: timezone, step_minutes: int
    ) -> list[SlotEntity]:
        start_of_day_local = datetime.combine(day, datetime.min.time(), tz)
        end_of_day_local = start_of_day_local + timedelta(days=1)
        events = self._get_events_for_day(user, start_of_day_local)
        slots = []
        current_time = start_of_day_local
        while current_time < end_of_day_local:
            slot_end_time = current_time + timedelta(minutes=step_minutes)
            is_free = not any(
                event.start_time.astimezone(tz) < slot_end_time
                and event.end_time.astimezone(tz) > current_time
                for event in events
            )
            slots.append(
                SlotEntity(
                    start_time=current_time, end_time=slot_end_time, is_free=is_free
                )
            )
            current_time = slot_end_time
        return slots
