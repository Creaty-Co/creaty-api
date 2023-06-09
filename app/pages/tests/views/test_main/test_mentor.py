from app.base.tests.views.base import BaseViewTest
from app.mentors.tests.factories import MentorFactory
from app.pages.models import PageMentors
from app.pages.tests.factories.page import PageFactory, PageMentorsFactory


class PagesMainMentorTest(BaseViewTest):
    mentor_id: int

    @property
    def path(self):
        return f"/pages/main/mentors/{self.mentor_id}/"

    def test_patch(self):
        self.become_staff()
        page = PageFactory()
        mentor = MentorFactory()
        self.mentor_id = mentor.id
        self._test('patch', status=200)
        self.assert_model(
            PageMentors, {'page': page.id, 'mentor': mentor.id, 'index': 0}
        )

    def test_delete(self):
        self.become_staff()
        page_mentors = PageMentorsFactory()
        mentor = page_mentors.mentor
        self.mentor_id = mentor.id
        self._test('delete')
        self.assert_equal(PageMentors.objects.count(), 0)
