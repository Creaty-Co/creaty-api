from rest_framework.response import Response

from app.base.views import BaseView
from app.bookings.services.book import BookService
from app.users.permissions import AuthenticatedPermission


class CalBookView(BaseView):
    permissions_map = {'post': [AuthenticatedPermission]}

    def post(self):
        book_service = BookService()
        serializer = self.get_valid_serializer()
        return Response(data=book_service.book(serializer.data, self.request.user))
