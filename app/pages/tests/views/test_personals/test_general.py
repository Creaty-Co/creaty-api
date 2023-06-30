from app.base.tests.views.base import BaseViewTest
from app.mentors.tests.factories import MentorFactory
from app.tags.tests.factories import TagFactory


class PagesPersonalTest(BaseViewTest):
    shortcut: str

    @property
    def path(self):
        return f"/pages/personal/{self.shortcut}/"

    def test_get(self):
        page = TagFactory().pages.first()
        self.shortcut = page.tag.shortcut
        # tag without mentor: will be hidden
        page.tags.add(TagFactory())
        # tag with mentor, but doesn't apply to the page: will be hidden
        TagFactory().mentors.add(MentorFactory())
        # tag with mentor: will be visible
        tag = TagFactory()
        tag.mentors.add(MentorFactory())
        page.tags.add(tag)
        self._test('get', {'tags': [{'id': tag.id}]})
