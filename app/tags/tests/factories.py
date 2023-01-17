import factory

from app.base.tests.factories.base import BaseFactory
from app.base.tests.fakers import Faker
from app.tags.models import Category, Tag


class CategoryFactory(BaseFactory):
    icon = factory.django.ImageField()
    title = Faker('english_word')
    shortcut = Faker('slug')

    class Meta:
        model = Category


class TagFactory(BaseFactory):
    category = factory.SubFactory(CategoryFactory)
    title = Faker('english_word')
    shortcut = Faker('slug')

    class Meta:
        model = Tag
