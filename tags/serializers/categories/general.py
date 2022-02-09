from rest_framework import serializers

from tags.models import Category
from tags.serializers.general import ListTagsSerializer


class TagsCategoriesSerializer(serializers.ModelSerializer):
    tags = ListTagsSerializer(many=True, source='tag_set')
    
    class Meta:
        model = Category
        fields = ['id', 'title', 'tags']
