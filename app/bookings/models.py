from typing import Final

from django.db import models
from django.utils import timezone

from app.base.money import Money
from app.mentors.models import Mentor


class AbstractBooking(models.Model):
    mentor: Mentor
    name = models.TextField()
    email = models.EmailField()
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)

    EVENT_TYPE: str
    DURATION: int

    class Meta:
        abstract = True

    def __str__(self):
        booking_type = type(self).__name__.rstrip('Booking')
        return f"{booking_type}: {self.name} ({self.email})"

    @property
    def price(self) -> Money:
        raise NotImplementedError


class TrialBooking(AbstractBooking):
    mentor = models.ForeignKey(
        'mentors.Mentor', models.CASCADE, related_name='free_bookings'
    )

    EVENT_TYPE = 'trial'
    DURATION = 15

    @property
    def price(self):
        return Money(0)


class HourlyBooking(AbstractBooking):
    mentor = models.ForeignKey(
        'mentors.Mentor', models.CASCADE, related_name='hourly_bookings'
    )

    EVENT_TYPE = 'hourly'
    DURATION = 60

    @property
    def price(self):
        return self.mentor.price


class PackageBooking(AbstractBooking):
    mentor = models.ForeignKey(
        'mentors.Mentor', models.CASCADE, related_name='package_bookings'
    )
    package = models.ForeignKey(
        'mentors.Package', models.CASCADE, related_name='bookings'
    )

    EVENT_TYPE = 'package'
    DURATION = 60

    @property
    def price(self):
        package = self.package
        return self.mentor.price * package.lessons_count * (1 - package.discount / 100)


booking_model_by_event_type: Final[dict[str, type[AbstractBooking]]] = {
    _booking_model.EVENT_TYPE: _booking_model
    for _booking_model in (TrialBooking, HourlyBooking, PackageBooking)
}
