from enum import Enum
from typing import Final

from app.bookings.entites.booking_type import BookingTypeEntity
from app.bookings.models import HourlyBooking, TrialBooking


class BookingTypeEnum(Enum):
    TRIAL: Final[BookingTypeEntity] = BookingTypeEntity(
        title='Trial meet', duration_minutes=15, model=TrialBooking
    )
    HOURLY: Final[BookingTypeEntity] = BookingTypeEntity(
        title='Hourly meet', duration_minutes=60, model=HourlyBooking
    )
    # FIXME: package is a separate type ?
    # PACKAGE: Final[BookingTypeEntity] = BookingTypeEntity(
    #     title='Hourly meet', duration_minutes=60, model=PackageBooking
    # )
