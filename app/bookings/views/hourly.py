from app.bookings.serializers.hourly import BookingsHourlySerializer
from app.bookings.views.base import BaseBookingsView


class BookingsHourlyView(BaseBookingsView):
    serializer_map = {'post': BookingsHourlySerializer}
