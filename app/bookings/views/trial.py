from app.base.views import BaseView
from app.bookings.serializers.trial import BookingsTrialSerializer


class BookingsTrialView(BaseView):
    serializer_map = {'post': BookingsTrialSerializer}

    def post(self):
        return self.create()
