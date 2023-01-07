from app.base.serializers.base import BaseModelSerializer
from app.geo.models import Country


class GeoCountriesSerializer(BaseModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'code', 'flag_unicode', 'name']
