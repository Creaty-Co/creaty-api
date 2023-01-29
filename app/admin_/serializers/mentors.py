from app.base.enums.currency import Currency
from app.base.serializers.base import BaseModelSerializer
from app.geo.models import Country
from app.mentors.models import Mentor, MentorInfo
from app.pages.models import Page


class _ListAdminMentorsInfoSerializer(BaseModelSerializer):
    class Meta:
        model = MentorInfo
        fields = ['trial_meeting', 'city']


class _ListAdminMentorsCountrySerializer(BaseModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class _ListAdminMentorsPagesSerializer(BaseModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'tag', 'category']


class ListAdminMentorsSerializer(BaseModelSerializer):
    info = _ListAdminMentorsInfoSerializer()
    country = _ListAdminMentorsCountrySerializer()
    pages = _ListAdminMentorsPagesSerializer(many=True, source='page_set')

    class Meta:
        model = Mentor
        extra_kwargs = {'price_currency': {'help_text': Currency.help_text}}
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
