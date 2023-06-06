from django.db import models


class AbstractBooking(models.Model):
    name = models.TextField()
    email = models.EmailField()
    description = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        booking_type = type(self).__name__.rstrip('Booking')
        return f"{booking_type}: {self.name} ({self.email})"


class TrialBooking(AbstractBooking):
    mentor = models.ForeignKey(
        'mentors.Mentor', models.CASCADE, related_name='free_bookings'
    )


class HourlyBooking(AbstractBooking):
    mentor = models.ForeignKey(
        'mentors.Mentor', models.CASCADE, related_name='hourly_bookings'
    )


class PackageBooking(AbstractBooking):
    mentor = models.ForeignKey(
        'mentors.Mentor', models.CASCADE, related_name='package_bookings'
    )
    package = models.ForeignKey(
        'mentors.Package', models.CASCADE, related_name='bookings'
    )
