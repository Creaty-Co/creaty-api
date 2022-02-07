from rest_framework import serializers

from mentors.serializers.general import MentorsSerializer
from pages.models import Page
from tags.serializers.general import TagsSerializer


class PagesMainSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True, source='tag_set')
    mentors = MentorsSerializer(many=True, source='mentor_set')
    
    class Meta:
        model = Page
        fields = ['id', 'tags', 'mentors']
