from app.base.tests.views.base import BaseViewTest
from app.geo.tests.factories.language import LanguageFactory


class GeoLanguageTest(BaseViewTest):
    path = '/geo/languages/'

    def test_get(self):
        language = LanguageFactory()
        self._test('get', {'count': 1, 'results': [{'id': language.id}]})
