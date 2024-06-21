from datetime import datetime

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework.response import Response

from app.base.serializers.fields.timezone import TimezoneField
from app.base.utils.schema import extend_schema
from app.base.views import BaseView
from app.bookings.serializers.slots.trial import (
    QueryParamsGETBookingsSlotsTrialSerializer,
    GETBookingsSlotsTrialSerializer,
)
from app.bookings.services.factories.slots import BookingSlotsFactory
from app.users.permissions import AuthenticatedPermission


class BookingsSlotsTrialView(BaseView):
    permissions_map = {'get': [AuthenticatedPermission]}
    serializer_map = {'get': GETBookingsSlotsTrialSerializer}

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='day',
                type=OpenApiTypes.DATE,
                description="The date parameter, default is today's date",
                default=datetime.today().strftime('%Y-%m-%d'),
            ),
            OpenApiParameter(
                name='timezone',
                type=OpenApiTypes.REGEX,
                pattern=TimezoneField.TIMEZONE_REGEX_PATTERN.pattern,
                description=(
                    "The timezone offset in the format ±hh:mm, default is +00:00"
                ),
                default='+00:00',
            ),
            OpenApiParameter(
                name='step_minutes',
                type=OpenApiTypes.INT,
                description="The slots step in minutes, default is 15",
                default=15,
            ),
        ]
    )
    def get(self):
        slots_factory = BookingSlotsFactory()

        query_params_serializer = QueryParamsGETBookingsSlotsTrialSerializer(
            data=self.request.query_params
        )
        query_params_serializer.is_valid()
        params = query_params_serializer.validated_data

        slots = slots_factory.create_slots_for_day(
            user=self.request.user,
            day=params['day'],
            tz=params['timezone'],
            step_minutes=params['step_minutes'],
        )

        serializer = self.get_serializer(instance={'slots': slots})
        return Response(data=serializer.data)
