from app.base.tests.views.base import BaseViewTest
from app.mentors.tests.factories import MentorFactory


class MentorsTest(BaseViewTest):
    path = '/mentors/'

    def test_get(self):
        MentorFactory()
        self._test('get', {'count': 1})
