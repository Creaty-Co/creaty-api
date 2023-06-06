from typing import Final

from app.base.services.cache import Cacher
from app.users.verification.code_generators.symbolic import SymbolicCodeGenerator
from app.users.verification.verifiers.email import EmailVerifier

register_verifier: Final = EmailVerifier(
    'email-verify',
    'email/register.html',
    Cacher('register', timeout=60 * 60 * 24),
    SymbolicCodeGenerator(10),
)

password_reset_verifier: Final = EmailVerifier(
    'reset-password',
    'email/password_reset.html',
    Cacher('password_reset', timeout=60 * 30),
    SymbolicCodeGenerator(10),
)
