from rest_framework.mixins import ListModelMixin

from base.views.base import BaseView
from geo.models import Country


class GeoCountriesView(ListModelMixin, BaseView):
    serializer_classes = {'get': GeoCountriesSerializer}
    queryset = Country.objects.all()
    
    def get(self, request):
        return self.list(request)
