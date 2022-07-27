from rest_framework import serializers

from pages.models import Locale


class PagesLocaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locale
        fields = ['json']
