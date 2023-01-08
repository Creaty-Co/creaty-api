import factory
from django.contrib.auth.hashers import make_password

from app.account.enums.users import UserType
from app.account.models import User
from app.base.tests.fakers import Faker


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    raw_password: str

    type = UserType.ADMIN
    email = Faker('email')
    password = Faker('password')
    first_name = Faker('first_name')
    last_name = Faker('last_name')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        raw_password = kwargs['password']
        obj = super()._create(
            model_class, *args, **kwargs | {'password': make_password(raw_password)}
        )
        obj.raw_password = raw_password
        return obj
