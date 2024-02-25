from django.db.models import Count

from app.mentors.models import Mentor
from app.pages.models import Page, PageMentors
from app.tags.models import Category, Tag


class PageService:
    MENTORS_COUNT = 20
    MAX_TAGS_COUNT = 20

    @property
    def main(self) -> Page:
        main_page, is_created = Page.objects.get_or_create(tag=None, category=None)
        if is_created:
            mentor_qs = Mentor.objects.filter(is_draft=False).order_by('?').nocache()
            tags_qs = Tag.objects.order_by('?').nocache()
            for index, mentor in enumerate(mentor_qs[: self.MENTORS_COUNT]):
                PageMentors.objects.create(page=main_page, mentor=mentor, index=index)
            main_page.tags.set(tags_qs[: self.MAX_TAGS_COUNT])
        return main_page

    def get_or_create(self, tag_or_category: Tag | Category) -> Page:
        if isinstance(tag_or_category, Tag):
            page, is_created = Page.objects.get_or_create(tag=tag_or_category)
        else:
            page, is_created = Page.objects.get_or_create(category=tag_or_category)
        if is_created:
            self.fill_random(page)
        return page

    def fill_random(self, page: Page) -> None:
        mentor_qs = Mentor.objects.filter(is_draft=False).order_by('?').nocache()
        tags_qs = (
            Tag.objects.annotate(Count('mentors'))
            .exclude(mentors__count=0)
            .order_by('?')
            .nocache()
        )
        if page.tag is None:
            mentors = set(
                mentor_qs.filter(tags__categories=page.category)[: self.MENTORS_COUNT]
            )
        else:
            tags_qs = tags_qs.exclude(id=page.tag.id)
            mentors = set(mentor_qs[: self.MENTORS_COUNT])
        if len(mentors) < self.MENTORS_COUNT:
            remaining_mentor_qs = mentor_qs.exclude(id__in={m.id for m in mentors})
            mentors |= set(remaining_mentor_qs[: self.MENTORS_COUNT - len(mentors)])
        for index, mentor in enumerate(mentors):
            PageMentors.objects.create(page=page, mentor=mentor, index=index)
        page.tags.set(tags_qs[: self.MAX_TAGS_COUNT])
