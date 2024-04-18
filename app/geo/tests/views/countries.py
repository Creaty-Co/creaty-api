from app.base.tests.views.base import BaseViewTest
from app.geo.tests.factories.country import CountryFactory


class GeoCountriesTest(BaseViewTest):
    def test_get(self):
        CountryFactory()
