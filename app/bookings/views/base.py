from rest_framework.response import Response

from app.base.notificators.emails.base import BaseEmailNotifier
from app.base.services.email.senders.base import BaseEmailSender
from app.base.views import BaseView
from app.bookings.models import AbstractBooking
from app.bookings.senders.admin import AdminBookingSender
from app.users.services.admin.notifiers.staff import StaffEmailNotifier


class BaseBookingsView(BaseView):
    def post(self):
        serializer = self.get_valid_serializer()
        booking: AbstractBooking = serializer.save()
        user_notifier = BaseEmailNotifier(
            email_sender=BaseEmailSender(template_name='email/mentor-request.html')
        )
        user_notifier.notify(
            [
                user_notifier.Notification(
                    email=booking.email, context={'booking': booking}
                )
            ]
        )
        admin_notifier = StaffEmailNotifier(email_sender=AdminBookingSender())
        notifications = admin_notifier.get_notifications()
        for notification in notifications:
            notification.context['booking'] = booking
        admin_notifier.notify(notifications)
        return Response(serializer.data, status=201)
