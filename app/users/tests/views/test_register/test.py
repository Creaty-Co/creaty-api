from unittest.mock import Mock

from django.core import mail
from django.utils.crypto import get_random_string

from app.base.tests.fakers import fake
from app.base.tests.views.base import BaseViewTest
from app.platform.services.auth import PlatformAuthService
from app.users.models import User
from app.users.regisration import registerer
from app.users.serializers.register.general import (
    POSTUsersRegisterSerializer,
    PUTUsersRegisterSerializer,
)
from app.users.tests.factories import UserFactory


class UsersRegisterTest(BaseViewTest):
    path = '/users/register/'

    me_data = None

    def test_post(self):
        email = fake.email()
        self._test(
            'post',
            {
                'access': lambda a: isinstance(a, str),
                'refresh': lambda r: isinstance(r, str),
            },
            {
                'first_name': fake.first_name(),
                'email': email,
                'password': fake.password(),
            },
            201,
        )
        self.assert_equal(len(mail.outbox), 1)
        self.assert_equal(mail.outbox[0].to, [email])
        self.assert_model(User, {'is_verified': False, 'has_discount': False})

    def test_post_warn_409_email_already_exists(self):
        user = UserFactory()
        self._test(
            'post',
            POSTUsersRegisterSerializer.WARNINGS[409],
            {
                'first_name': fake.first_name(),
                'email': user.email,
                'password': fake.password(),
            },
        )
        self.assert_equal(len(mail.outbox), 0)

    def test_put(self):
        user = UserFactory(is_verified=False, has_discount=False)
        code = get_random_string(10)
        registerer.verifier.cache.set((user.email, None), code)
        registerer.verifier.cache.set(code, user.email)
        PlatformAuthService.register = Mock()
        self._test(
            'put',
            {
                'access': lambda a: isinstance(a, str),
                'refresh': lambda r: isinstance(r, str),
            },
            {'code': code},
            status=200,
        )
        self.assert_model(User, {'is_verified': True, 'has_discount': True})
        self.assert_equal(len(mail.outbox), 1)

    def test_put_warn_408(self):
        UserFactory(is_verified=False, has_discount=False)
        code = get_random_string(10)
        self._test('put', PUTUsersRegisterSerializer.WARNINGS[408], {'code': code})
        self.assert_model(User, {'is_verified': False, 'has_discount': False})
        self.assert_equal(len(mail.outbox), 0)
