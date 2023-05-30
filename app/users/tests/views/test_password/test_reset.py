from django.core import mail
from django.utils.crypto import get_random_string

from app.base.tests.fakers import fake
from app.base.tests.views.base import BaseViewTest
from app.users.models import User
from app.users.password_reset import password_resetter
from app.users.serializers.password.reset import (
    POSTUsersPasswordResetSerializer,
    PUTUsersPasswordResetSerializer,
)
from app.users.tests.factories import UserFactory


class UsersPasswordResetTest(BaseViewTest):
    path = '/users/password/reset/'

    me_data = None

    def test_post(self):
        user = UserFactory()
        self._test('post', data={'email': user.email}, status=204)
        self.assert_equal(len(mail.outbox), 1)
        self.assert_equal(mail.outbox[0].to, [user.email])
        self.assert_model(User, {'password': user.password})

    def test_post_warn_404(self):
        email = fake.email()
        self._test(
            'post', POSTUsersPasswordResetSerializer.WARNINGS[404], {'email': email}
        )
        self.assert_equal(len(mail.outbox), 0)

    def test_put(self):
        user = UserFactory()
        code = get_random_string(10)
        password_resetter.verifier.cache.set((user.email, None), code)
        password_resetter.verifier.cache.set(code, user.email)
        new_password = fake.password()
        self._test(
            'put',
            {
                'access': lambda a: isinstance(a, str),
                'refresh': lambda r: isinstance(r, str),
            },
            {'code': code, 'new_password': new_password},
            status=200,
        )
        self.assert_true(User.objects.get().check_password(new_password))

    def test_put_warn_408(self):
        user = UserFactory()
        code = get_random_string(10)
        new_password = fake.password()
        self._test(
            'put',
            PUTUsersPasswordResetSerializer.WARNINGS[408],
            {'code': code, 'new_password': new_password},
        )
        self.assert_model(User, {'password': user.password})
