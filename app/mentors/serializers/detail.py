from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from app.base.enums.currency import Currency
from app.base.serializers.base import BaseModelSerializer
from app.geo.models import Country, Language
from app.mentors.models import Mentor, MentorInfo, Package
from app.tags.serializers.general import ListTagsSerializer


class _RetrieveMentorInfoLanguagesSerializer(BaseModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name_native']


class _RetrieveMentorInfoSerializer(BaseModelSerializer):
    languages = _RetrieveMentorInfoLanguagesSerializer(
        many=True, read_only=True, source='language_set'
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


class _RetrieveMentorCountrySerializer(BaseModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'flag_unicode']


class _RetrieveMentorPackagesSerializer(BaseModelSerializer):
    class Meta:
        model = Package
        fields = ['id', 'lessons_count', 'discount']


class RetrieveMentorSerializer(BaseModelSerializer):
    info = _RetrieveMentorInfoSerializer()
    country = _RetrieveMentorCountrySerializer()
    tags = ListTagsSerializer(many=True, source='tag_set')
    packages = _RetrieveMentorPackagesSerializer(many=True)

    class Meta:
        model = Mentor
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
            'packages',
            'info',
        ]


class _UpdateMentorInfoSerializer(BaseModelSerializer):
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


class _UpdateMentorPackagesSerializer(BaseModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # FIXME
        self.parent = None
        self.partial = False

    class Meta:
        model = Package
        fields = ['lessons_count', 'discount']


class UpdateMentorSerializer(BaseModelSerializer):
    info = _UpdateMentorInfoSerializer(write_only=True)
    price_currency = serializers.ChoiceField(
        choices=Currency.choices,
        help_text=Currency.help_text,
        write_only=True,
    )
    packages = _UpdateMentorPackagesSerializer(
        many=True, write_only=True, partial=False
    )
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

    def update(self, mentor, vd):
        if vd.get('info'):
            vd['info'] = _UpdateMentorInfoSerializer(partial=True).update(
                MentorInfo.objects.get(mentor=mentor), vd.pop('info')
            )
        if 'packages' in vd:
            Package.objects.filter(mentor=mentor).delete()
            for package in vd.pop('packages'):
                Package.objects.create(mentor=mentor, **package)
        mentor = super().update(mentor, vd)
        return mentor
