from typing import Final

from app.bookings.models import (
    AbstractBooking,
    HourlyBooking,
    PackageBooking,
    TrialBooking,
)
from app.cal.models import CalEventType


class BookingModelService:
    MODELS: tuple[type[AbstractBooking]] = (TrialBooking, HourlyBooking, PackageBooking)

    def __init__(self):
        self.cal_event_type_manager = CalEventType.objects
        self.model_by_event_type: Final[dict[str, type[AbstractBooking]]] = {
            _booking_model.EVENT_TYPE: _booking_model for _booking_model in self.MODELS
        }

    def get_by_event_type(self, event_type: str) -> type[AbstractBooking]:
        return self.model_by_event_type[event_type]

    def get_by_event_type_id(self, event_type_id: int) -> type[AbstractBooking]:
        return self.get_by_event_type(
            self.cal_event_type_manager.get(id=event_type_id).slug
        )
