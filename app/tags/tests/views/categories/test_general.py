from app.base.tests.views.base import BaseViewTest
from app.mentors.tests.factories import MentorFactory
from app.tags.tests.factories import CategoryFactory, TagFactory


class TagsCategoriesTest(BaseViewTest):
    path = '/tags/categories/'

    def test_get(self):
        # category without tags: will be hidden
        CategoryFactory()
        # category with tag without mentors: will be hidden
        CategoryFactory().tags.add(TagFactory())
        # category with tags with mentor: will be visible
        tag = TagFactory()
        tag.mentors.add(MentorFactory())
        CategoryFactory().tags.add(tag, TagFactory())
        self._test('get', {'count': 1, 'results': [{'tags': [{'id': tag.id}]}]})
