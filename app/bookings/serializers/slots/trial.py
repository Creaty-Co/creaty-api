from datetime import datetime

from rest_framework import serializers

from app.base.serializers.base import BaseSerializer
from app.base.serializers.fields.timezone import TimezoneField


class _SlotGETBookingsSlotsTrialSerializer(BaseSerializer):
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    is_free = serializers.BooleanField()


class GETBookingsSlotsTrialSerializer(BaseSerializer):
    slots = _SlotGETBookingsSlotsTrialSerializer(many=True)


class QueryParamsGETBookingsSlotsTrialSerializer(BaseSerializer):
    day = serializers.DateField(default=datetime.today())
    timezone = TimezoneField(default='+00:00')
    step_minutes = serializers.IntegerField(min_value=5, max_value=60, default=15)
