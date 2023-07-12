from app.bookings.serializers.trial import BookingsTrialSerializer
from app.bookings.views.base import BaseBookingsView


class BookingsTrialView(BaseBookingsView):
    serializer_map = {'post': BookingsTrialSerializer}
