from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from pages.serializers.main import PagesMainSerializer


class PagesPersonalSerializer(PagesMainSerializer):
    title = serializers.SerializerMethodField()
    
    class Meta(PagesMainSerializer.Meta):
        fields = PagesMainSerializer.Meta.fields[:]
        fields.insert(1, 'title')
    
    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, page):
        if page.tag is None:
            return page.category.title
        return page.tag.title
