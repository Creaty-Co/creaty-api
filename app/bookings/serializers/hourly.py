from rest_framework import serializers

from app.base.serializers.base import BaseModelSerializer
from app.bookings.models import HourlyBooking
from app.mentors.models import Mentor


class BookingsHourlySerializer(BaseModelSerializer):
    mentor = serializers.SlugRelatedField(
        slug_field='slug', queryset=Mentor.objects.all()
    )

    class Meta:
        model = HourlyBooking
        write_only_fields = [
            'mentor',
            'name',
            'email',
            'description',
        ]
        read_only_fields = ['id']
