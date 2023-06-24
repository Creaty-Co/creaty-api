from typing import Final

from app.users.password_reset.resetter import PasswordResetter
from app.users.verification import (
    mentor_password_reset_verifier,
    password_reset_verifier,
)

password_resetter: Final[PasswordResetter] = PasswordResetter(
    user_verifier=password_reset_verifier,
    mentor_verifier=mentor_password_reset_verifier,
)
