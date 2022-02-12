from django.conf import settings
from drf_base64.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.permissions import AllowAny

from base.utils.functions import choices_to_help_text
from geo.models import Country, Language
from mentors.models import Mentor, MentorInfo, Package
from tags.models import Tag


class _MentorsTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']


class _MentorsCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'flag_unicode']


class ListMentorsSerializer(serializers.ModelSerializer):
    country = _MentorsCountrySerializer()
    tags = _MentorsTagsSerializer(many=True, source='tag_set')
    avatar = Base64ImageField()
    
    class Meta:
        model = Mentor
        extra_kwargs = {
            'price_currency': {
                'help_text': choices_to_help_text(settings.CURRENCY_CHOICES)
            }
        }
        fields = [
            'id', 'avatar', 'company', 'profession', 'first_name', 'last_name', 'price',
            'price_currency', 'country', 'tags'
        ]


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


class _CreateMentorsPackagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ['lessons_count', 'discount']


class CreateMentorsSerializer(serializers.ModelSerializer):
    info = _MentorsCreateInfoSerializer(write_only=True)
    price_currency = serializers.ChoiceField(
        choices=settings.CURRENCY_CHOICES,
        help_text=choices_to_help_text(settings.CURRENCY_CHOICES), write_only=True
    )
    packages = _CreateMentorsPackagesSerializer(many=True, write_only=True)
    
    class Meta:
        model = Mentor
        wo = {'write_only': True}
        extra_kwargs = {
            'id': {}, 'info': {}, 'avatar': wo, 'company': wo, 'profession': wo,
            'first_name': wo, 'last_name': wo, 'price': wo, 'price_currency': {},
            'tag_set': wo, 'country': wo, 'packages': {}
        }
        fields = list(extra_kwargs.keys())
    
    def create(self, vd):
        vd['info'] = _MentorsCreateInfoSerializer().create(vd.pop('info'))
        mentor = super().create(vd)
        for package in vd['packages']:
            Package.objects.create(mentor=mentor, **package)
