from app.base.tests.fakers import fake
from app.base.tests.views.base import BaseViewTest
from app.users.tests.factories import UserFactory


class UsersTokenTest(BaseViewTest):
    path = '/users/token/'

    me_data = None

    def test_post(self):
        user = UserFactory()
        self._test(
            'post',
            data={
                'email': user.email,
                'password': user.raw_password,
            },
            status=200,
        )

    def test_post_error_401_user_not_exist(self):
        self._test(
            'post',
            data={
                'email': fake.email(),
                'password': fake.random_string(),
            },
            status=401,
        )

    def test_post_error_401_invalid_password(self):
        user = UserFactory()
        self._test(
            'post',
            data={
                'email': user.email,
                'password': fake.random_string(),
            },
            status=401,
        )
