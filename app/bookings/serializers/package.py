from rest_framework import serializers

from app.base.serializers.base import BaseModelSerializer
from app.bookings.models import PackageBooking
from app.mentors.models import Mentor


class BookingsPackageSerializer(BaseModelSerializer):
    mentor = serializers.SlugRelatedField(
        slug_field='slug', queryset=Mentor.objects.all()
    )

    class Meta:
        model = PackageBooking
        write_only_fields = [
            'mentor',
            'name',
            'email',
            'description',
            'package',
        ]
        read_only_fields = ['id']
