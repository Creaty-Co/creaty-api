import factory
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from social_django.models import UserSocialAuth

from app.base.tests.factories.base import BaseFactory
from app.base.tests.fakers import Faker, fake
from app.users.models import User


class UserFactory(BaseFactory):
    email = Faker('email')
    password = Faker('password')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    has_discount = True
    is_verified = True

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


class GroupFactory(BaseFactory):
    class Meta:
        model = Group

    name = Faker('english_word')


class UserSocialAuthFactory(BaseFactory):
    class Meta:
        model = UserSocialAuth

    user = factory.SubFactory(UserFactory)
    provider = Faker('word')
    uid = Faker('uuid4')
    extra_data = factory.LazyFunction(
        lambda: {
            'auth_time': int(fake.unix_time()),
            'expires': fake.random_int(min=3600, max=7200),
            'access_token': fake.uuid4(),
            'refresh_token': fake.uuid4(),
        }
    )
