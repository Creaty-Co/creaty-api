from app.mentors.tests.factories import MentorFactory
from app.pages.services.page import PageService
from app.pages.tests.views.test_main.test_general import PagesMainTest
from app.tags.tests.factories import CategoryFactory, TagFactory


class PagesPersonalTest(PagesMainTest):
    shortcut: str

    @property
    def path(self):
        return f"/pages/personal/{self.shortcut}/"

    def test_get(self):
        page = CategoryFactory().page
        self.shortcut = page.category.shortcut
        self._test_get(page)

    def test_get_category_page_with_over_max_mentors(self):
        for _ in range(PageService.MENTORS_COUNT + 1):
            MentorFactory()
        page = CategoryFactory().page
        self.shortcut = page.category.shortcut
        self.assert_equal(PageService.MENTORS_COUNT, page.mentors.count())
        self._test_get(page)

    def test_get_tag_page_with_over_max_mentors(self):
        for _ in range(PageService.MENTORS_COUNT + 1):
            MentorFactory()
        page = TagFactory().page
        self.shortcut = page.tag.shortcut
        self.assert_equal(PageService.MENTORS_COUNT, page.mentors.count())
        self._test_get(page)
