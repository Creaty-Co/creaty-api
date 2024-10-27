from abc import ABC, abstractmethod

from app.calendar.entites.calendar_event import CalendarEventEntity
from app.calendar.models import CalendarEvent


class BaseCalendarEventFactory(ABC):
    def __init__(self):
        self.calendar_event_manager = CalendarEvent.objects

    @abstractmethod
    def create_event(self, calendar_event_entity: CalendarEventEntity) -> CalendarEvent:
        raise NotImplementedError
