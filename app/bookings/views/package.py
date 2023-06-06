from app.base.views import BaseView
from app.bookings.serializers.package import BookingsPackageSerializer


class BookingsPackageView(BaseView):
    serializer_map = {'post': BookingsPackageSerializer}

    def post(self):
        return self.create()
