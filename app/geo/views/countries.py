from app.base.views import BaseView
from app.geo.models import Country
from app.geo.serializers.countries import GeoCountriesSerializer


class GeoCountriesView(BaseView):
    many = True
    serializer_map = {'get': GeoCountriesSerializer}
    queryset = Country.objects.all()

    def get(self):
        return self.list()
