from django.core import mail
from django.utils.crypto import get_random_string

from app.base.tests.fakers import fake
from app.base.tests.views.base import BaseViewTest
from app.users.models import User
from app.users.regisration import registerer
from app.users.serializers.register.general import POSTUsersRegisterSerializer
from app.users.tests.factories import UserFactory
from app.users.verification import register_verifier


class UsersRegisterTest(BaseViewTest):
    path = '/users/register/'

    me_data = None

    def test_get(self):
        user = UserFactory(is_verified=False, has_discount=False)
        code = get_random_string(10)
        register_verifier.cache.set((code, None), user.email)
        response = self.get(path=f"{self.path}?email={user.email}&code={code}")
        self.assert_response(response, 302)
        self.assert_equal(response.url, registerer.successful_url)
        self.assert_model(User, {'is_verified': True, 'has_discount': True})

    def test_get_failure_email_not_found(self):
        code = get_random_string(10)
        response = self.get(path=f"{self.path}?email={fake.email()}&code={code}")
        self.assert_response(response, 302)
        self.assert_equal(response.url, registerer.failure_url)

    def test_get_failure_invalid_code(self):
        user = UserFactory(is_verified=False, has_discount=False)
        code = get_random_string(10)
        response = self.get(path=f"{self.path}?email={user.email}&code={code}")
        self.assert_response(response, 302)
        self.assert_equal(response.url, registerer.failure_url)
        self.assert_model(User, {'is_verified': False, 'has_discount': False})

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
