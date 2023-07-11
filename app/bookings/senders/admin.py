from datetime import datetime, timedelta

from templated_mail.mail import BaseEmailMessage

from app.base.services.email.senders.base import BaseEmailSender
from app.bookings.models import AbstractBooking


class AdminBookingSender(BaseEmailSender):
    class ContextDict(BaseEmailSender.ContextDict):
        booking: AbstractBooking
        deadline: datetime
        type: str

    TEMPLATE_NAME: str = 'email/admin-request-product.html'
    DEADLINE_OFFSET = timedelta(days=1)

    def __init__(
        self, email_message_factory: type[BaseEmailMessage] = BaseEmailMessage
    ):
        super().__init__(self.TEMPLATE_NAME, email_message_factory)

    def _create_context(self, email, **kwargs) -> ContextDict:
        booking: AbstractBooking = kwargs['booking']
        kwargs['deadline'] = booking.created_at + self.DEADLINE_OFFSET
        kwargs['type'] = type(booking).__name__
        return super()._create_context(email, **kwargs)
