from app.base.tests.base import BaseTest
from app.pages.models import Page
from app.tags.tests.factories import CategoryFactory, TagFactory


class TagsSignalsTest(BaseTest):
    def test_tag_post_save_1(self):
        tag = TagFactory()
        self.assert_model(Page, {'tags': []}, tag=tag)

    def test_tag_post_save_2_without_mentors(self):
        TagFactory()
        tag = TagFactory()
        self.assert_model(Page, {'tags': []}, tag=tag)

    def test_tag_post_save_2(self):
        tag1 = TagFactory.with_mentors()
        tag2 = TagFactory()
        self.assert_model(Page, {'tags': [tag1]}, tag=tag2)

    def test_category_post_save(self):
        category = CategoryFactory.with_tags([TagFactory.with_mentors()])
        self.assert_model(Page, {'tags': list(category.tags.all())}, category=category)
