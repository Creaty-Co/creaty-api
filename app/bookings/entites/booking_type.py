from app.base.entities.base import BaseEntity
from app.bookings.models import AbstractBooking


class BookingTypeEntity(BaseEntity):
    title: str
    duration_minutes: int
    model: type[AbstractBooking]
