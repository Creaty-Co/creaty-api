from rest_framework import serializers

from geo.models import Country


class GeoCountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'code', 'flag_unicode', 'name']
