from app.base.tests.views.base import BaseViewTest
from app.mentors.tests.factories import MentorFactory
from app.pages.models import PageMentorSet
from app.pages.tests.factories.page import PageMentorSetFactory
from app.tags.tests.factories import CategoryFactory


class PagesPersonalMentorTest(BaseViewTest):
    shortcut: str
    mentor_id: int

    @property
    def path(self):
        return f"/pages/personal/{self.shortcut}/mentors/{self.mentor_id}/"

    def test_patch(self):
        category = CategoryFactory()
        page = category.page
        mentor = MentorFactory()
        self.shortcut = page.category.shortcut
        self.mentor_id = mentor.id
        self._test('patch')
        self.assert_model(
            PageMentorSet, {'page': page.id, 'mentor': mentor.id, 'index': 0}
        )

    def test_delete(self):
        category = CategoryFactory()
        page = category.page
        page_mentor_set = PageMentorSetFactory(page=page)
        mentor = page_mentor_set.mentor
        self.shortcut = page.category.shortcut
        self.mentor_id = mentor.id
        self._test('delete')
        self.assert_equal(PageMentorSet.objects.count(), 0)
