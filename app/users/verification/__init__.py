from typing import Final

from app.base.services.cache import Cacher
from app.users.verification.code_generators.symbolic import SymbolicCodeGenerator
from app.users.verification.email_senders.base import BaseVerificationEmailSender
from app.users.verification.email_senders.user import UserVerificationEmailSender
from app.users.verification.link_generators.email.code import CodeLinkGenerator
from app.users.verification.link_generators.email.mentor import MentorLinkGenerator
from app.users.verification.verifiers.email import EmailVerifier

register_verifier: Final[EmailVerifier] = EmailVerifier(
    verification_email_sender=BaseVerificationEmailSender(
        template_name='email/after-sign-up.html'
    ),
    cache=Cacher('register', timeout=60 * 60 * 24),
    code_generator=SymbolicCodeGenerator(10),
    link_generator=CodeLinkGenerator(path='email-verify'),
)

password_reset_verifier: Final[EmailVerifier] = EmailVerifier(
    verification_email_sender=BaseVerificationEmailSender(
        template_name='email/password-reset.html'
    ),
    cache=Cacher('password_reset', timeout=60 * 30),
    code_generator=SymbolicCodeGenerator(10),
    link_generator=CodeLinkGenerator(path='reset-password'),
)

mentor_password_reset_verifier: Final[EmailVerifier] = EmailVerifier(
    verification_email_sender=BaseVerificationEmailSender(
        template_name='email/password-reset.html'
    ),
    cache=Cacher('mentor_password_reset', timeout=60 * 30),
    code_generator=SymbolicCodeGenerator(10),
    link_generator=MentorLinkGenerator(path='reset-password'),
)
