from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from mentors.models import Mentor
from tags.models import Tag


class _MentorsTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']


class MentorsSerializer(serializers.ModelSerializer):
    country_flag = serializers.SerializerMethodField()
    tags = _MentorsTagsSerializer(many=True, source='tag_set')
    
    class Meta:
        model = Mentor
        fields = [
            'id', 'avatar', 'company', 'profession', 'first_name', 'last_name', 'price',
            'price_currency', 'country_flag', 'tags'
        ]
    
    @extend_schema_field(OpenApiTypes.STR)
    def get_country_flag(self, mentor):
        return mentor.country_flag
