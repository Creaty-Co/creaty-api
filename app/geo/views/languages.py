from app.base.views import BaseView
from app.geo.models import Language
from app.geo.serializers.languages import GeoLanguagesSerializer


class GeoLanguagesView(BaseView):
    many = True
    serializer_map = {'get': GeoLanguagesSerializer}
    queryset = Language.objects.all()

    def get(self):
        return self.list()
