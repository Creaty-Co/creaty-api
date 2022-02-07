from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from mentors.models import Mentor
from pages.models import Page
from tags.models import Tag


class _PageTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'shortcut', 'title']


class _PageMentorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ['id', 'shortcut', 'title'] # FIXME


class PagesMainSerializer(serializers.ModelSerializer):
    tags = _PageTagsSerializer(many=True, source='tag_set')
    mentors = _PageMentorsSerializer(many=True, source='mentor_set')
    
    class Meta:
        model = Page
        fields = ['id', 'tags', 'mentors']
