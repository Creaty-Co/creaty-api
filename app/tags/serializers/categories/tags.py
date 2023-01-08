from rest_framework.validators import UniqueValidator

from app.base.serializers.base import BaseModelSerializer
from app.tags.models import Category, Tag


class TagsCategoryTagsSerializer(BaseModelSerializer):
    class Meta:
        model = Tag
        wo = {'write_only': True}
        extra_kwargs = {
            'id': {},
            'shortcut': wo
            | {
                'validators': [
                    UniqueValidator(Tag.objects.all()),
                    UniqueValidator(Category.objects.all()),
                ]
            },
            'title_ru': wo,
            'title_en': wo,
        }
        fields = list(extra_kwargs.keys())
