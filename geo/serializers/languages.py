from rest_framework import serializers

from geo.models import Language


class GeoLanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'code', 'name', 'name_native']
