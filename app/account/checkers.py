from app.account.models import User
from app.base.checkers.base import BaseChecker


class AuthenticatedChecker(BaseChecker):
    InEntity = User

    def check(self, data: InEntity) -> bool:
        return getattr(data, 'is_authenticated', False)
