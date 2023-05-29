from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from app.base.enums.currency import Currency
from app.base.serializers.base import BaseModelSerializer
from app.geo.models import Country, Language
from app.mentors.models import Mentor, MentorInfo, Package
from app.tags.models import Tag


class _GETMentorsTagsSerializer(BaseModelSerializer):
    class Meta:
        model = Tag
        read_only_fields = ['id', 'shortcut', 'title']


class _GETMentorsCountrySerializer(BaseModelSerializer):
    class Meta:
        model = Country
        read_only_fields = ['id', 'flag_unicode']


class GETMentorsSerializer(BaseModelSerializer):
    country = _GETMentorsCountrySerializer()
    tags = _GETMentorsTagsSerializer(many=True, source='tag_set')

    class Meta:
        model = Mentor
        extra_kwargs = {'price_currency': {'help_text': Currency.help_text}}
        read_only_fields = [
            'id',
            'slug',
            'avatar',
            'company',
            'profession',
            'first_name',
            'last_name',
            'price',
            'price_currency',
            'country',
            'tags',
            'is_draft',
        ]


class _POSTMentorsInfoSerializer(BaseModelSerializer):
    languages = serializers.PrimaryKeyRelatedField(
        allow_empty=False,
        many=True,
        queryset=Language.objects.all(),
        source='language_set',
    )

    class Meta:
        model = MentorInfo
        extra_kwargs = {'price_currency': {'help_text': Currency.help_text}}
        write_only_fields = [
            'trial_meeting',
            'resume',
            'what_help',
            'experience',
            'languages',
            'city',
        ]


class _POSTMentorsPackagesSerializer(BaseModelSerializer):
    class Meta:
        model = Package
        write_only_fields = ['lessons_count', 'discount']


class POSTMentorsSerializer(BaseModelSerializer):
    info = _POSTMentorsInfoSerializer()
    price_currency = serializers.ChoiceField(
        choices=Currency.choices, help_text=Currency.help_text
    )
    packages = _POSTMentorsPackagesSerializer(many=True)
    avatar = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Mentor
        write_only_fields = [
            'info',
            'avatar',
            'company',
            'profession',
            'first_name',
            'last_name',
            'price',
            'price_currency',
            'tag_set',
            'country',
            'packages',
            'is_draft',
        ]

    def create(self, vd):
        vd['info'] = _POSTMentorsInfoSerializer().create(vd.pop('info'))
        tag_set = vd.pop('tag_set')
        packages = vd.pop('packages')
        mentor = Mentor.objects.create(**vd)
        mentor.tag_set.add(*tag_set)
        for package in packages:
            Package.objects.create(mentor=mentor, **package)
        return mentor
