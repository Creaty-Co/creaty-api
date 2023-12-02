from rest_framework.response import Response

from app.base.exceptions import ClientError
from app.base.parsers import ORJSONParser
from app.base.views import BaseView
from app.cal.services.schedule import CalScheduleService


class CalScheduleView(BaseView):
    def get(self):
        cal_schedule_service = CalScheduleService()
        input_ = self._parse_input()
        try:
            data = cal_schedule_service.get(input_)
        except cal_schedule_service.InputInvalidException as exc:
            raise ClientError("query param `input` is invalid") from exc
        return Response(data=data)

    def _parse_input(self) -> dict:
        json_parser = ORJSONParser()
        try:
            input_str: str = self.request.query_params['input']
        except KeyError as exc:
            raise ClientError("query param `input` is required") from exc
        return json_parser.parse(input_str)
