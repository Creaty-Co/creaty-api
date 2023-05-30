import base64
import random

from app.base.enums.currency import Currency
from app.base.tests.fakers import fake
from app.base.tests.views.base import BaseViewTest
from app.geo.tests.factories.country import CountryFactory
from app.geo.tests.factories.language import LanguageFactory
from app.mentors.models import Mentor
from app.mentors.tests.factories import MentorFactory
from app.tags.tests.factories import TagFactory


class MentorsTest(BaseViewTest):
    path = '/mentors/'

    def test_get(self):
        MentorFactory()
        self._test('get', {'count': 1})

    def test_post(self):
        self.become_staff()
        language = LanguageFactory()
        country = CountryFactory()
        tag = TagFactory()
        avatar = fake.image()
        self._test(
            'post',
            data={
                'info': {
                    'trial_meeting': random.randint(1, 10),
                    'resume': fake.english_text(),
                    'what_help': fake.english_text(),
                    'experience': fake.english_text(),
                    'languages': [language.id],
                    'city': fake.city(),
                },
                'avatar': (
                    b"data:application/"
                    + avatar.name.split('.')[-1].encode()
                    + b";base64,"
                    + base64.b64encode(avatar.read())
                ),
                'company': fake.company(),
                'profession': fake.english_text(),
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'price': random.randint(1_000, 10_000) / 100,
                'price_currency': fake.random_element(Currency),
                'tag_set': [tag.id],
                'country': country.id,
                'packages': [
                    {
                        'lessons_count': random.randint(2, 10),
                        'discount': random.randint(1, 99),
                    }
                ],
            },
        )
        self.assert_model(Mentor, {})
