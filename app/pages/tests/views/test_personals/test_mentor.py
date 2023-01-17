from app.base.tests.views.base import BaseViewTest
from app.mentors.tests.factories import MentorFactory
from app.pages.models import PageMentorSet
from app.tags.tests.factories import CategoryFactory


class PagesPersonalMentorTest(BaseViewTest):
    shortcut: str
    mentor_id: int

    @property
    def path(self):
        return f"/pages/personal/{self.shortcut}/mentors/{self.mentor_id}/"

    def test_patch_page_existed(self):
        category = CategoryFactory()
        page = category.page
        mentor = MentorFactory()
        self.shortcut = page.category.shortcut
        self.mentor_id = mentor.id
        self._test('patch')
        self.assert_model(PageMentorSet, {'page': page, 'mentor': mentor, 'index': 1})
