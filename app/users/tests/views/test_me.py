from app.base.tests.views.base import BaseViewTest
from app.users.models import User


class UsersMeTest(BaseViewTest):
    path = '/users/me/'

    def test_get(self):
        self._test('get', {'id': lambda id: self.assert_model(User, {'id': id})})
