from app.base.tests.views.base import BaseViewTest
from app.mentors.tests.factories import MentorFactory


class MentorTest(BaseViewTest):
    slug: str

    @property
    def path(self):
        return f"/mentors/{self.slug}/"

    def test_get(self):
        mentor = MentorFactory()
        self.slug = mentor.slug
        self._test('get')
