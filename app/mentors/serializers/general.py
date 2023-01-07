from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from app.base.enums.currency import Currency
from app.base.serializers.base import BaseModelSerializer
from app.geo.models import Country, Language
from app.mentors.models import Mentor, MentorInfo, Package
from app.tags.models import Tag


class _MentorsTagsSerializer(BaseModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'shortcut', 'title']


class _MentorsCountrySerializer(BaseModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'flag_unicode']


class ListMentorsSerializer(BaseModelSerializer):
    country = _MentorsCountrySerializer()
    tags = _MentorsTagsSerializer(many=True, source='tag_set')

    class Meta:
        model = Mentor
        extra_kwargs = {'price_currency': {'help_text': Currency.help_text}}
        fields = [
            'id',
            'avatar',
            'company',
            'profession',
            'first_name',
            'last_name',
            'price',
            'price_currency',
            'country',
            'tags',
        ]


class _MentorsCreateInfoSerializer(BaseModelSerializer):
    languages = serializers.PrimaryKeyRelatedField(
        allow_empty=False,
        many=True,
        queryset=Language.objects.all(),
        source='language_set',
    )

    class Meta:
        model = MentorInfo
        extra_kwargs = {'price_currency': {'help_text': Currency.help_text}}
        fields = [
            'trial_meeting',
            'resume',
            'what_help',
            'experience',
            'portfolio',
            'languages',
            'city_ru',
            'city_en',
        ]


class _CreateMentorsPackagesSerializer(BaseModelSerializer):
    class Meta:
        model = Package
        fields = ['lessons_count', 'discount']


class CreateMentorsSerializer(BaseModelSerializer):
    info = _MentorsCreateInfoSerializer(write_only=True)
    price_currency = serializers.ChoiceField(
        choices=Currency.choices,
        help_text=Currency.help_text,
        write_only=True,
    )
    packages = _CreateMentorsPackagesSerializer(many=True, write_only=True)
    avatar = Base64ImageField(write_only=True)

    class Meta:
        model = Mentor
        wo = {'write_only': True}
        extra_kwargs = {
            'id': {},
            'info': {},
            'avatar': wo,
            'company': wo,
            'profession': wo,
            'first_name': wo,
            'last_name': wo,
            'price': wo,
            'price_currency': {},
            'tag_set': wo,
            'country': wo,
            'packages': {},
        }
        fields = list(extra_kwargs.keys())

    def create(self, vd):
        vd['info'] = _MentorsCreateInfoSerializer().create(vd.pop('info'))
        tag_set = vd.pop('tag_set')
        packages = vd.pop('packages')
        mentor = Mentor.objects.create(**vd)
        mentor.tag_set.add(*tag_set)
        for package in packages:
            Package.objects.create(mentor=mentor, **package)
        return mentor
