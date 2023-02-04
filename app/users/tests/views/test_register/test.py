import random

from django.core import mail

from app.base.tests.fakers import fake
from app.base.tests.views.base import BaseViewTest
from app.users.models import User
from app.users.regisration import registerer
from app.users.serializers.register.general import UsersRegisterSerializer
from app.users.tests.factories import UserFactory
from app.users.verification import register_verifier


class UsersRegisterTest(BaseViewTest):
    path = '/users/register/'

    me_data = None

    def test_get(self):
        code = random.randint(100_000, 999_999)
        email = fake.email()
        payload = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': email,
            'password': fake.password(),
        }
        register_verifier.cache.set((code, payload), email)  # noqa:test
        response = self.get(path=f"{self.path}?email={email}&code={code}")
        self.assert_response(response, 302)
        self.assert_equal(response.url, registerer.successful_url)
        self.assert_model(User, {'email': email})

    def test_get_failure_email_not_found(self):
        code = random.randint(100_000, 999_999)
        payload = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'password': fake.password(),
        }
        register_verifier.cache.set(  # noqa:test
            (random.randint(100_000, 999_999), payload), fake.email()
        )
        response = self.get(path=f"{self.path}?email={fake.email()}&code={code}")
        self.assert_response(response, 302)
        self.assert_equal(response.url, registerer.failure_url)
        self.assert_equal(User.objects.count(), 0)

    def test_get_failure_invalid_code(self):
        email = fake.email()
        payload = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': email,
            'password': fake.password(),
        }
        register_verifier.cache.set(  # noqa:test
            (random.randint(100_000, 999_999), payload), email
        )
        response = self.get(
            path=f"{self.path}?email={email}&code={random.randint(100_000, 999_999)}"
        )
        self.assert_response(response, 302)
        self.assert_equal(response.url, registerer.failure_url)
        self.assert_equal(User.objects.count(), 0)

    def test_post(self):
        self._test(
            'post',
            data={
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'email': fake.email(),
                'password': fake.password(),
            },
            status=204,
        )
        self.assert_equal(len(mail.outbox), 1)

    def test_post_error_409_email_already_exists(self):
        user = UserFactory()
        self._test(
            'post',
            UsersRegisterSerializer.WARNINGS[409],
            {
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'email': user.email,
                'password': fake.password(),
            },
        )
