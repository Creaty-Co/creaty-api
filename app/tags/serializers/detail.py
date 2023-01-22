from rest_framework.validators import UniqueValidator

from app.base.serializers.base import BaseModelSerializer
from app.tags.models import Category, Tag


class UpdateTagSerializer(BaseModelSerializer):
    class Meta:
        model = Tag
        wo = {'write_only': True}
        extra_kwargs = {
            'shortcut': wo
            | {
                'validators': [
                    UniqueValidator(Tag.objects.all()),
                    UniqueValidator(Category.objects.all()),
                ]
            },
            'title': wo,
        }
        fields = list(extra_kwargs.keys())
