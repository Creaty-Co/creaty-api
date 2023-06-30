from app.base.tests.fakers import fake
from app.base.tests.views.base import BaseViewTest
from app.mentors.tests.factories import MentorFactory
from app.tags.models import Tag
from app.tags.tests.factories import CategoryFactory, TagFactory


class TagsTest(BaseViewTest):
    path = '/tags/'

    def test_get(self):
        TagFactory()  # tag without mentor: will be hidden
        TagFactory().mentors.add(MentorFactory())  # tag with mentor: will be visible
        self._test('get', {'count': 1})

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
