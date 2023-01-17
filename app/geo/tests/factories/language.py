from app.base.tests.factories.base import BaseFactory
from app.base.tests.fakers import Faker
from app.geo.models import Language


class LanguageFactory(BaseFactory):
    code = Faker('language_code')
    name = Faker('language_name')
    name_native = Faker('language_name')

    class Meta:
        model = Language
