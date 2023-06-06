from app.base.views import BaseView
from app.bookings.serializers.hourly import BookingsHourlySerializer


class BookingsHourlyView(BaseView):
    serializer_map = {'post': BookingsHourlySerializer}

    def post(self):
        return self.create()
