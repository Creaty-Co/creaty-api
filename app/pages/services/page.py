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
            self._fill_random(page)
        return page

    def _fill_random(self, page: Page) -> None:
        raw_mentor_qs = Mentor.objects.filter(is_draft=False).order_by('?').nocache()
        tags_qs = (
            Tag.objects.annotate(Count('mentors'))
            .exclude(mentors__count=0)
            .order_by('?')
            .nocache()
        )
        if page.tag is None:
            mentor_qs = raw_mentor_qs.filter(tags__categories=page.category)
        else:
            mentor_qs = raw_mentor_qs.filter(tags=page.tag)
            tags_qs = tags_qs.exclude(id=page.tag.id)
        mentors = set(mentor_qs)
        if len(mentors) < self.MENTORS_COUNT:
            remaining_mentor_qs = raw_mentor_qs.exclude(id__in={m.id for m in mentors})
            mentors |= set(remaining_mentor_qs[: self.MENTORS_COUNT - len(mentors)])
        for index, mentor in enumerate(mentors):
            PageMentors.objects.create(page=page, mentor=mentor, index=index)
        page.tags.set(tags_qs[: self.MAX_TAGS_COUNT])
