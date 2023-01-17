from app.base.tests.views.base import BaseViewTest
from app.mentors.models import Mentor, MentorInfo
from app.mentors.tests.factories import MentorFactory


class MentorTest(BaseViewTest):
    pk: int

    @property
    def path(self):
        return f"/mentors/{self.pk}/"

    def test_delete(self):
        mentor = MentorFactory()
        self.pk = mentor.id
        self._test('delete')
        self.assert_equal(Mentor.objects.count(), 0)
        self.assert_equal(MentorInfo.objects.count(), 0)
