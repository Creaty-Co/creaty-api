from mentors.models import Mentor
from pages.models import Page, PageMentorSet
from tags.models import Category, Tag


class PageService:
    MAX_MENTORS_COUNT = 20
    MAX_TAGS_COUNT = 20
    
    @property
    def main(self) -> Page:
        main_page, is_created = Page.objects.get_or_create(tag=None, category=None)
        if is_created:
            mentor_qs = Mentor.objects.order_by('?').nocache()
            tags_qs = Tag.objects.order_by('?').nocache()
            for index, mentor in enumerate(mentor_qs[:self.MAX_MENTORS_COUNT]):
                PageMentorSet.objects.create(page=main_page, mentor=mentor, index=index)
            main_page.tag_set.set(tags_qs[:self.MAX_TAGS_COUNT])
        return main_page
    
    def get_or_create(self, tag_or_category: Tag | Category) -> Page:
        if isinstance(tag_or_category, Tag):
            page, is_created = Page.objects.get_or_create(tag=tag_or_category)
        else:
            page, is_created = Page.objects.get_or_create(category=tag_or_category)
        if is_created:
            self._fill_random(page)
        return page
    
    def _fill_random(self, page: Page) -> None:
        mentor_qs = Mentor.objects.order_by('?').nocache()
        tags_qs = Tag.objects.order_by('?').nocache()
        if page.tag is None:
            mentor_qs = mentor_qs.filter(tag_set__category=page.category)
        else:
            mentor_qs = mentor_qs.filter(tag_set=page.tag)
            tags_qs = tags_qs.exclude(id=page.tag.id)
        for index, mentor in enumerate(mentor_qs[:self.MAX_MENTORS_COUNT]):
            PageMentorSet.objects.create(page=page, mentor=mentor, index=index)
        page.tag_set.set(tags_qs[:self.MAX_TAGS_COUNT])
