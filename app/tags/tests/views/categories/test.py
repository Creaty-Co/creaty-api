from app.base.tests.views.base import BaseViewTest


class TagsCategoriesTest(BaseViewTest):
    path = '/tags/categories/'

    def test_get(self):
        # MAYBE: check categories without tags or mentors when user is default / admin
        self._test('get')
