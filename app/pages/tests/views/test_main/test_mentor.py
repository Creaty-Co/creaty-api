from app.base.tests.views.base import BaseViewTest
from app.mentors.tests.factories import MentorFactory
from app.pages.models import PageMentorSet
from app.pages.tests.factories.page import PageFactory, PageMentorSetFactory


class PagesMainMentorTest(BaseViewTest):
    mentor_id: int

    @property
    def path(self):
        return f"/pages/main/mentors/{self.mentor_id}/"

    def test_patch(self):
        page = PageFactory()
        mentor = MentorFactory()
        self.mentor_id = mentor.id
        self._test('patch')
        self.assert_model(
            PageMentorSet, {'page': page.id, 'mentor': mentor.id, 'index': 0}
        )

    def test_delete(self):
        page_mentor_set = PageMentorSetFactory()
        mentor = page_mentor_set.mentor
        self.mentor_id = mentor.id
        self._test('delete')
        self.assert_equal(PageMentorSet.objects.count(), 0)
