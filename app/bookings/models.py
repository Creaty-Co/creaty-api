from django.db import models
from django.utils import timezone

from app.base.money import Money
from app.mentors.models import Mentor


class AbstractBooking(models.Model):
    mentor: Mentor
    name = models.TextField()
    email = models.EmailField()
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

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

    @property
    def price(self) -> Money:
        return Money(0)


class HourlyBooking(AbstractBooking):
    mentor = models.ForeignKey(
        'mentors.Mentor', models.CASCADE, related_name='hourly_bookings'
    )

    @property
    def price(self) -> Money:
        return self.mentor.price


class PackageBooking(AbstractBooking):
    mentor = models.ForeignKey(
        'mentors.Mentor', models.CASCADE, related_name='package_bookings'
    )
    package = models.ForeignKey(
        'mentors.Package', models.CASCADE, related_name='bookings'
    )

    @property
    def price(self):
        return self.mentor.price * (1 - self.package.discount / 100)
