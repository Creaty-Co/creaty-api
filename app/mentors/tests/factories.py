import random

import factory

from app.base.tests.factories.base import BaseFactory
from app.base.tests.fakers import Faker
from app.geo.tests.factories.country import CountryFactory
from app.mentors.models import Mentor, MentorInfo


class MentorInfoFactory(BaseFactory):
    resume = Faker('english_text')
    what_help = Faker('english_text')
    experience = Faker('english_text')
    city = Faker('city')

    class Meta:
        model = MentorInfo


class MentorFactory(BaseFactory):
    info = factory.SubFactory(MentorInfoFactory)
    avatar = factory.django.ImageField()
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    company = Faker('company')
    profession = Faker('english_text')
    price = factory.LazyAttribute(lambda m: random.randint(1, 1000))
    country = factory.SubFactory(CountryFactory)
    is_draft = False

    class Meta:
        model = Mentor


class PackageFactory(BaseFactory):
    mentor = factory.SubFactory(MentorFactory)
    lessons_count = factory.LazyAttribute(lambda m: random.randint(2, 10))
    discount = factory.LazyAttribute(lambda m: random.randint(2, 99))
