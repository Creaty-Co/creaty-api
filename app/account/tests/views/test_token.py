from app.account.models import Token
from app.account.serializers.token import POST_UsersTokenSerializer
from app.base.tests.fakers import fake
from app.base.tests.views.base import BaseViewTest


class UsersTokenTest(BaseViewTest):
    path = '/account/token/'

    def test_post_success(self):
        user = self.me
        self.client.logout()
        self._test(
            'post',
            data={
                'email': user.email,
                'password': user.raw_password,
            },
        )

    def test_user_not_exist(self):
        self._test(
            'post',
            POST_UsersTokenSerializer.WARNINGS[401],
            {
                'email': fake.email(),
                'password': fake.english_word(),
            },
        )

    def test_delete_user(self):
        self._test('delete')
        self.assert_equal(Token.objects.count(), 0)
