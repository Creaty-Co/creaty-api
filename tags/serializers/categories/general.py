from rest_framework import serializers

from tags.models import Category
from tags.serializers.general import TagsSerializer


class TagsCategoriesSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True, source='tag_set', read_only=True)
    
    class Meta:
        model = Category
        extra_kwargs = {'id': {}, 'title': {'read_only': True}}
        fields = list(extra_kwargs.keys()) + ['tags']
