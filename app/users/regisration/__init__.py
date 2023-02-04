from typing import Final

from app.users.regisration.registerer import Registerer
from app.users.verification import register_verifier

registerer: Final = Registerer(register_verifier)
