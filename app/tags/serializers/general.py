from app.base.serializers.base import BaseModelSerializer
from app.tags.models import Tag


class ListTagsSerializer(BaseModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'shortcut', 'title']
