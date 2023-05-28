from typing import Final

from app.users.password_reset.resetter import PasswordResetter
from app.users.verification import password_reset_verifier

password_resetter: Final = PasswordResetter(password_reset_verifier)
