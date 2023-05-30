from app.base.tests.fakers import fake
from app.base.tests.views.base import BaseViewTest
from app.tags.models import Tag
from app.tags.tests.factories import CategoryFactory


class TagsTest(BaseViewTest):
    path = '/tags/'

    def test_post(self):
        self.become_staff()
        category = CategoryFactory()
        self._test(
            'post',
            data={
                'shortcut': fake.first_name(),
                'title': fake.first_name(),
                'categories': [category.id],
            },
        )
        self.assert_model(Tag, {})
