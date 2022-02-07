from rest_framework import serializers

from tags.models import Category
from tags.serializers.general import TagsSerializer


class TagsCategoriesSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True, source='tag_set')
    
    class Meta:
        model = Category
        fields = ['id', 'title', 'tags']
