import random

import factory

from app.base.tests.factories.base import BaseFactory
from app.base.tests.fakers import Faker
from app.forms.models import Form
from app.forms.models.choices import FormType


class FormFactory(BaseFactory):
    type = factory.LazyAttribute(lambda _: random.choice(list(FormType)))
    description = Faker('paragraph')
    post_send = Faker('paragraph')

    class Meta:
        model = Form
