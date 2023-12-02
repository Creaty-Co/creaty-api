from app.base.logs import debug
from app.base.renderers import ORJSONRenderer
from app.bookings.models import TrialBooking
from app.bookings.services.model import BookingModelService
from app.cal.requesters.cal_api import CalAPIRequester


class CalScheduleService:
    class InputInvalidException(Exception):
        pass

    def __init__(self):
        # FIXME: getting admin username from DB
        self.admin_username: str = '1'
        self.cal_api_requester = CalAPIRequester()
        self.json_renderer = ORJSONRenderer()
        self.booking_model_service = BookingModelService()

    def get(self, input_: dict) -> dict:
        self._check_input(input_)
        event_type: str = input_['json']['eventTypeSlug']
        if event_type == TrialBooking.EVENT_TYPE:
            # add admin username
            input_['json']['usernameList'].append(self.admin_username)
        booking_model = self.booking_model_service.get_by_event_type(event_type)
        input_['json']['duration'] = booking_model.DURATION
        input_str = self.json_renderer.render(input_).decode()
        debug(f"{input_str = }")
        return self.cal_api_requester.get_schedule(input_str)

    def _check_input(self, input_: dict) -> None:
        try:
            event_type = input_['json']['eventTypeSlug']
            assert isinstance(event_type, str)
            assert event_type in self.booking_model_service.model_by_event_type.keys()
            assert isinstance(input_['json']['usernameList'], list)
        except (AssertionError, KeyError, ValueError) as exc:
            raise self.InputInvalidException from exc
