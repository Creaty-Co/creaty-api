from django.conf import settings
from drf_base64.fields import Base64ImageField
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from base.utils.functions import choices_to_help_text
from geo.models import Language
from mentors.models import Mentor, MentorInfo
from tags.models import Tag


class _MentorsTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']


class MentorsListSerializer(serializers.ModelSerializer):
    country_flag = serializers.SerializerMethodField()
    tags = _MentorsTagsSerializer(many=True, source='tag_set')
    avatar = Base64ImageField()
    
    class Meta:
        model = Mentor
        fields = [
            'id', 'avatar', 'company', 'profession', 'first_name', 'last_name', 'price',
            'price_currency', 'country_flag', 'tags'
        ]
    
    @extend_schema_field(OpenApiTypes.STR)
    def get_country_flag(self, mentor):
        return mentor.country.flag_unicode


class _MentorsCreateInfoSerializer(serializers.ModelSerializer):
    languages = serializers.PrimaryKeyRelatedField(
        allow_empty=False, many=True, queryset=Language.objects.all(),
        source='language_set'
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


class MentorsCreateSerializer(serializers.ModelSerializer):
    info = _MentorsCreateInfoSerializer(write_only=True)
    price_currency = serializers.ChoiceField(
        choices=settings.CURRENCY_CHOICES,
        help_text=choices_to_help_text(settings.CURRENCY_CHOICES), write_only=True
    )
    
    class Meta:
        model = Mentor
        wo = {'write_only': True}
        extra_kwargs = {
            'id': {}, 'info': {}, 'avatar': wo, 'company': wo, 'profession': wo,
            'first_name': wo, 'last_name': wo, 'price': wo, 'price_currency': {},
            'tag_set': wo, 'country': wo
        }
        fields = list(extra_kwargs.keys())
    
    def create(self, vd):
        vd['info'] = _MentorsCreateInfoSerializer().create(vd.pop('info'))
        return super().create(vd)
