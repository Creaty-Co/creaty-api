import factory

from app.account.models import Token
from app.account.tests.factories.users import UserFactory
from app.base.tests.factories.base import BaseFactory


class TokenFactory(BaseFactory):
    class Meta:
        model = Token

    user = factory.SubFactory(UserFactory)
