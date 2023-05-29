from django.core import mail

from app.base.tests.fakers import fake
from app.base.tests.views.base import BaseViewTest
from app.users.serializers.register.resend import POSTUsersRegisterResendSerializer
from app.users.tests.factories import UserFactory


class UsersRegisterResendTest(BaseViewTest):
    path = '/users/register/resend/'

    me_data = None

    def test_post(self):
        user = UserFactory(is_verified=False, has_discount=False)
        self._test('post', data={'email': user.email})
        self.assert_equal(len(mail.outbox), 1)
        self.assert_equal(mail.outbox[0].to, [user.email])

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
