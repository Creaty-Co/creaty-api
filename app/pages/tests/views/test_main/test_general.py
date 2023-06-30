from app.base.tests.views.base import BaseViewTest
from app.mentors.tests.factories import MentorFactory
from app.pages.tests.factories.page import PageFactory
from app.tags.tests.factories import TagFactory


class PagesMainTest(BaseViewTest):
    path = '/pages/main/'

    def _test_get(self, page):
        # tag without mentor: will be hidden
        page.tags.add(TagFactory())
        # tag with mentor, but doesn't apply to the page: will be hidden
        TagFactory().mentors.add(MentorFactory())
        # tag with draft mentor: will be hidden
        tag = TagFactory()
        tag.mentors.add(MentorFactory(is_draft=True))
        page.tags.add(tag)
        # tag with mentor: will be visible
        tag = TagFactory()
        tag.mentors.add(MentorFactory())
        page.tags.add(tag)
        self._test('get', {'tags': [{'id': tag.id}]})

    def test_get(self):
        self._test_get(PageFactory())
