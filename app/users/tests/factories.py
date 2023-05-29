import factory
from django.contrib.auth.hashers import make_password

from app.base.tests.fakers import Faker
from app.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    email = Faker('email')
    password = Faker('password')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    has_discount = True
    is_verified = True
    is_superuser = True

    raw_password: str

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        raw_password = kwargs['password']
        obj = super()._create(
            model_class, *args, **kwargs | {'password': make_password(raw_password)}
        )
        obj.raw_password = raw_password
        return obj
