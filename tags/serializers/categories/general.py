from rest_framework import serializers

from tags.models import Category
from tags.serializers.general import ListTagsSerializer


class ListTagsCategoriesSerializer(serializers.ModelSerializer):
    tags = ListTagsSerializer(many=True, source='tag_set')
    
    class Meta:
        model = Category
        fields = ['id', 'title', 'tags']


class CreateTagsCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        wo = {'write_only': True}
        extra_kwargs = {'id': {}, 'shortcut': wo, 'title_ru': wo, 'title_en': wo}
        fields = list(extra_kwargs.keys())
