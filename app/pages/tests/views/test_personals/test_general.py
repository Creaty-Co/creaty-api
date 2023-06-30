from app.pages.tests.views.test_main.test_general import PagesMainTest
from app.tags.tests.factories import CategoryFactory


class PagesPersonalTest(PagesMainTest):
    shortcut: str

    @property
    def path(self):
        return f"/pages/personal/{self.shortcut}/"

    def test_get(self):
        page = CategoryFactory().pages.first()
        self.shortcut = page.category.shortcut
        self._test_get(page)
