import random

import factory
from factory.django import DjangoModelFactory

from geo.models import Country
from mentors.models import Mentor, MentorInfo


class MentorInfoFactory(DjangoModelFactory):
    resume = factory.Faker('text')
    what_help = factory.Faker('text')
    experience = factory.Faker('text')
    portfolio = factory.Faker('text')
    city = factory.Faker('city')
    
    class Meta:
        model = MentorInfo


class MentorFactory(DjangoModelFactory):
    info = factory.SubFactory(MentorInfoFactory)
    avatar = factory.django.ImageField()
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    price = factory.LazyAttribute(lambda m: random.randint(1, 1000))
    country = factory.LazyAttribute(lambda m: random.choice(Country.objects.all()))
    
    class Meta:
        model = Mentor
