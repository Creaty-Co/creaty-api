import re

from django.core import mail
from django.utils.crypto import get_random_string

from app.base.tests.fakers import fake
from app.base.tests.views.base import BaseViewTest
from app.mentors.tests.factories import MentorFactory
from app.users.models import User
from app.users.password_reset import password_resetter
from app.users.serializers.password.reset import (
    POSTUsersPasswordResetSerializer,
    PUTUsersPasswordResetSerializer,
)
from app.users.tests.factories import UserFactory


class UsersPasswordResetTest(BaseViewTest):
    USER_RESET_PASSWORD_LINK_REGEX = r"https://.+/reset-password/{code}"
    MENTOR_RESET_PASSWORD_LINK_REGEX = (
        r"https://.+/reset-password/{code}\?first_name=.+"
    )

    path = '/users/password/reset/'

    me_data = None

    def _test_post(self, user, link_regex):
        self._test('post', data={'email': user.email}, status=204)
        self.assert_equal(len(mail.outbox), 1)
        email_message = mail.outbox[0]
        self.assert_equal(email_message.to, [user.email])
        self.assert_is_not_none(
            re.fullmatch(
                link_regex.format(**email_message.context),
                email_message.context['link'],
            )
        )
        self.assert_model(User, {'password': user.password})

    def test_post_user(self):
        user = UserFactory()
        self._test_post(user, self.USER_RESET_PASSWORD_LINK_REGEX)

    def test_post_mentor_with_password(self):
        mentor = MentorFactory()
        self._test_post(mentor, self.USER_RESET_PASSWORD_LINK_REGEX)

    def test_post_mentor_without_password(self):
        mentor = MentorFactory()
        mentor.set_password(None)
        mentor.save()
        self._test_post(mentor, self.MENTOR_RESET_PASSWORD_LINK_REGEX)

    def test_post_warn_404(self):
        email = fake.email()
        self._test(
            'post', POSTUsersPasswordResetSerializer.WARNINGS[404], {'email': email}
        )
        self.assert_equal(len(mail.outbox), 0)

    def _test_put(self, user, verifier):
        code = get_random_string(10)
        verifier.cache.set((user.email, None), code)
        verifier.cache.set(code, user.email)
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
        self.assert_equal(len(mail.outbox), 1)

    def test_put_user(self):
        user = UserFactory()
        verifier = password_resetter.user_verifier
        self._test_put(user, verifier)

    def test_put_mentor(self):
        user = MentorFactory().user_ptr
        verifier = password_resetter.mentor_verifier
        self._test_put(user, verifier)

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
        self.assert_equal(len(mail.outbox), 0)
