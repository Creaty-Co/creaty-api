from rest_framework.mixins import CreateModelMixin, ListModelMixin

from base.views.base import BaseView
from tags.models import Category
from tags.serializers.categories.general import (
    CreateTagsCategoriesSerializer, ListTagsCategoriesSerializer
)


class TagsCategoriesView(ListModelMixin, CreateModelMixin, BaseView):
    serializer_classes = {
        'get': ListTagsCategoriesSerializer, 'post': CreateTagsCategoriesSerializer
    }
    queryset = Category.objects.prefetch_related('tag_set').all()
    
    def get(self, request):
        return self.list(request)
