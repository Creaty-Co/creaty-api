from django.conf import settings
from rest_framework import serializers

from base.utils.functions import choices_to_help_text
from geo.models import Country
from mentors.models import Mentor, MentorInfo
from pages.models import Page


class _ListAdminMentorsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorInfo
        fields = ['trial_meeting', 'city_ru', 'city_en']


class _ListAdminMentorsCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class _ListAdminMentorsPagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'tag', 'category']


class ListAdminMentorsSerializer(serializers.ModelSerializer):
    info = _ListAdminMentorsInfoSerializer()
    country = _ListAdminMentorsCountrySerializer()
    pages = _ListAdminMentorsPagesSerializer(many=True, source='page_set')

    class Meta:
        model = Mentor
        extra_kwargs = {
            'price_currency': {
                'help_text': choices_to_help_text(settings.CURRENCY_CHOICES)
            }
        }
        fields = [
            'id',
            'info',
            'avatar',
            'company',
            'profession',
            'first_name',
            'last_name',
            'price',
            'price_currency',
            'country',
            'pages',
        ]
