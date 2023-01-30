from app.base.checkers.base import BaseChecker
from app.users.models import User


class AuthenticatedChecker(BaseChecker):
    InEntity = User

    def check(self, data: InEntity) -> bool:
        return getattr(data, 'is_authenticated', False)
