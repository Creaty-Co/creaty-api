from typing import Iterable

import factory

from app.base.tests.factories.base import BaseFactory
from app.base.tests.fakers import Faker
from app.mentors.models import Mentor
from app.mentors.tests.factories import MentorFactory
from app.tags.models import Category, CategoryTag, Tag


class CategoryFactory(BaseFactory):
    icon = factory.django.ImageField()
    title = Faker('english_word')
    shortcut = Faker('slug')

    class Meta:
        model = Category

    @classmethod
    def with_tags(
        cls, tags_or_count: Iterable[Tag] | int = 1, category: Category = None
    ) -> Category:
        category = category or cls()
        match tags_or_count:
            case int():
                for _ in range(tags_or_count):
                    CategoryTag.objects.create(category=category, tag=TagFactory())
            case _:
                for tag in tags_or_count:
                    CategoryTag.objects.create(category=category, tag=tag)
        return category


class TagFactory(BaseFactory):
    title = Faker('english_word')
    shortcut = Faker('slug')

    class Meta:
        model = Tag

    @classmethod
    def with_mentors(
        cls, mentors_or_count: Iterable[Mentor] | int = 1, tag: Tag = None
    ) -> Tag:
        tag = tag or cls()
        match mentors_or_count:
            case int():
                for _ in range(mentors_or_count):
                    tag.mentors.add(MentorFactory())
            case _:
                for mentor in mentors_or_count:
                    tag.mentors.add(mentor)
        return tag

    @classmethod
    def with_categories(
        cls, categories_or_count: Iterable[Category] | int = 1, tag: Tag = None
    ) -> Tag:
        tag = tag or cls()
        match categories_or_count:
            case int():
                for _ in range(categories_or_count):
                    CategoryTag.objects.create(tag=tag, category=CategoryFactory())
            case _:
                for category in categories_or_count:
                    CategoryTag.objects.create(tag=tag, category=category)
        return tag
