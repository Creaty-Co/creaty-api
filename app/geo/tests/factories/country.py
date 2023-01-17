from app.base.tests.factories.base import BaseFactory
from app.base.tests.fakers import Faker
from app.geo.models import Country


class CountryFactory(BaseFactory):
    code = Faker('country_code')
    flag_unicode = Faker('language_code')
    name = Faker('country')

    class Meta:
        model = Country
