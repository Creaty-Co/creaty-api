from app.bookings.serializers.package import BookingsPackageSerializer
from app.bookings.views.base import BaseBookingsView


class BookingsPackageView(BaseBookingsView):
    serializer_map = {'post': BookingsPackageSerializer}
