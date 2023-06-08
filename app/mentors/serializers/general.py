from app.base.enums.currency import Currency
from app.base.serializers.base import BaseModelSerializer
from app.geo.models import Country
from app.mentors.models import Mentor
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
    tags = _GETMentorsTagsSerializer(many=True)

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
            'link',
        ]
