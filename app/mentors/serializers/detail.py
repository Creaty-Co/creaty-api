from app.base.enums.currency import Currency
from app.base.serializers.base import BaseModelSerializer
from app.geo.models import Country, Language
from app.mentors.models import Mentor, Package
from app.tags.serializers.general import ListTagsSerializer


class _RetrieveMentorInfoLanguagesSerializer(BaseModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name_native']


class _RetrieveMentorInfoSerializer(BaseModelSerializer):
    languages = _RetrieveMentorInfoLanguagesSerializer(many=True, read_only=True)

    class Meta:
        model = Mentor
        fields = [
            'trial_meeting',
            'resume',
            'what_help',
            'experience',
            'languages',
            'city',
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
    tags = ListTagsSerializer(many=True)
    packages = _RetrieveMentorPackagesSerializer(many=True)

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
            'packages',
            'info',
            'is_draft',
        ]

    def to_representation(self, instance):
        instance.info = instance
        return super().to_representation(instance)