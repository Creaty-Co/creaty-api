import factory

from app.base.tests.factories.base import BaseFactory
from app.mentors.tests.factories import MentorFactory
from app.pages.models import Page, PageMentors


class PageFactory(BaseFactory):
    class Meta:
        model = Page


class PageMentorsFactory(BaseFactory):
    page = factory.SubFactory(PageFactory)
    mentor = factory.SubFactory(MentorFactory)
    index = factory.sequence(lambda _: _)

    class Meta:
        model = PageMentors
