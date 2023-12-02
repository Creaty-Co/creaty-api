from datetime import datetime

from app.bookings.models import AbstractBooking, TrialBooking
from app.bookings.services.model import BookingModelService
from app.cal.models import CalEventType
from app.cal.requesters.cal_api import CalAPIRequester
from app.users.models import User


class BookService:
    class DataInvalidException(Exception):
        pass

    def __init__(self):
        self.booking_model_service = BookingModelService()
        self.cal_api_requester = CalAPIRequester()

    def book(self, data: dict, mentee: User) -> dict:
        try:
            booking_model = self.booking_model_service.get_by_event_type_id(
                data['eventTypeId']
            )
        except CalEventType.DoesNotExist as exc:
            raise self.DataInvalidException from exc
        self._check_duration(data, booking_model)
        if booking_model == TrialBooking:
            pass  # FIXME: add operator
        data['responses']['email'] = mentee.email
        return self.cal_api_requester.post_book_event(data)

    def _check_duration(self, data: dict, booking_model: type[AbstractBooking]) -> None:
        try:
            expected_duration = booking_model.DURATION
            start_at = datetime.fromisoformat(data['start'])
            end_at = datetime.fromisoformat(data['end'])
            actual_duration = (end_at - start_at).seconds / 60
            assert expected_duration == actual_duration
        except AssertionError as exc:
            raise self.DataInvalidException from exc
