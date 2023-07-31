from rest_framework.response import Response

from app.base.notificators.emails.base import BaseEmailNotifier
from app.base.services.email.senders.base import BaseEmailSender
from app.base.views import BaseView
from app.bookings.models import AbstractBooking
from app.bookings.senders.operator import OperatorBookingSender
from app.users.models import User
from app.users.services.admin.notifiers.operator import OperatorsEmailNotifier


class BaseBookingsView(BaseView):
    def post(self):
        serializer = self.get_valid_serializer()
        booking: AbstractBooking = serializer.save()
        operator_notifier = OperatorsEmailNotifier(email_sender=OperatorBookingSender())
        notifications = operator_notifier.get_notifications()
        for notification in notifications:
            notification.context['booking'] = booking
        operator_notifier.notify(notifications)
        if not User.objects.filter(email=booking.email).exists():
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
        return Response(serializer.data, status=201)
