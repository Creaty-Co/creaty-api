from rest_framework.mixins import ListModelMixin

from base.views.base import BaseView
from geo.models import Language
from geo.serializers.languages import GeoLanguagesSerializer


class GeoLanguagesView(ListModelMixin, BaseView):
    serializer_classes = {'get': GeoLanguagesSerializer}
    queryset = Language.objects.all()

    def get(self, request):
        return self.list(request)
