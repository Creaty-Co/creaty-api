from typing import Final

from app.users.notificators.email import UsersEmailNotifier
from app.users.regisration.registerer import Registerer
from app.users.services.email.senders.user import UserEmailSender
from app.users.verification import register_verifier

registerer: Final[Registerer] = Registerer(
    verifier=register_verifier,
    confirm_notifier=UsersEmailNotifier(
        email_sender=UserEmailSender(template_name='email/account-verified.html')
    ),
)
