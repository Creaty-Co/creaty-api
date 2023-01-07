from app.base.serializers.base import BaseModelSerializer
from app.geo.models import Language


class GeoLanguagesSerializer(BaseModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'code', 'name', 'name_native']
