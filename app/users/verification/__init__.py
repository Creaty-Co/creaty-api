from typing import Final

from app.base.services.cache import Cacher
from app.users.verification.code_generators.numeric import NumericCodeGenerator
from app.users.verification.verifiers.base import BaseVerifier
from app.users.verification.verifiers.email import EmailVerifier

register_verifier: Final[BaseVerifier] = EmailVerifier(
    'register',
    'email/register.html',
    Cacher('register', timeout=60 * 60),
    NumericCodeGenerator(100000, 999999),
)
