from django.conf import settings
from rest_framework import serializers

from base.utils.functions import choices_to_help_text
from geo.models import Country, Language
from mentors.models import Mentor, MentorInfo
from tags.serializers.general import ListTagsSerializer


class _MentorInfoLanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name_native']


class _MentorInfoSerializer(serializers.ModelSerializer):
    languages = _MentorInfoLanguagesSerializer(
        many=True, read_only=True, source='language_set'
    )
    
    class Meta:
        model = MentorInfo
        extra_kwargs = {
            'price_currency': {
                'help_text': choices_to_help_text(settings.CURRENCY_CHOICES)
            }
        }
        fields = [
            'trial_meeting', 'resume', 'what_help', 'experience', 'portfolio',
            'languages', 'city_ru', 'city_en'
        ]


class _MentorCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'flag_unicode']


class MentorSerializer(serializers.ModelSerializer):
    info = _MentorInfoSerializer()
    country = _MentorCountrySerializer()
    tags = ListTagsSerializer(many=True, source='tag_set')
    
    class Meta:
        model = Mentor
        fields = [
            'id', 'avatar', 'company', 'profession', 'first_name', 'last_name', 'price',
            'price_currency', 'country', 'tags', 'info'
        ]
