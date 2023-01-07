import random

import factory
from factory.django import DjangoModelFactory

from app.tags.models import Category, Tag


class CategoryFactory(DjangoModelFactory):
    icon = factory.django.ImageField()
    title = factory.Faker('word')
    shortcut = factory.Faker('slug')

    class Meta:
        model = Category


class TagFactory(DjangoModelFactory):
    category = factory.LazyAttribute(lambda t: random.choice(Category.objects.all()))
    title = factory.Faker('word')
    shortcut = factory.Faker('slug')

    class Meta:
        model = Tag
