import random

from django.core import mail

from app.base.tests.fakers import fake
from app.base.tests.views.base import BaseViewTest
from app.users.serializers.register.resend import POSTUsersRegisterResendSerializer
from app.users.tests.factories import UserFactory
from app.users.verification import register_verifier


class UsersRegisterResendTest(BaseViewTest):
    path = '/users/register/resend/'

    me_data = None

    def test_post(self):
        code = random.randint(100_000, 999_999)
        email = fake.email()
        payload = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': email,
            'password': fake.password(),
        }
        register_verifier.cache.set((code, payload), email)  # noqa:test
        self._test('post', data={'email': email})
        self.assert_equal(len(mail.outbox), 1)
        self.assert_equal(mail.outbox[0].to, [email])

    def test_post_warn_404(self):
        self._test(
            'post',
            POSTUsersRegisterResendSerializer.WARNINGS[404],
            {'email': fake.email()},
        )
        self.assert_equal(len(mail.outbox), 0)

    def test_post_warn_409(self):
        user = UserFactory()
        self._test(
            'post',
            POSTUsersRegisterResendSerializer.WARNINGS[409],
            {'email': user.email},
        )
        self.assert_equal(len(mail.outbox), 0)
