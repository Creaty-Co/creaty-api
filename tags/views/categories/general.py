from rest_framework.mixins import ListModelMixin

from base.views.base import BaseView
from tags.models import Category
from tags.serializers.categories.general import TagsCategoriesSerializer


class TagsCategoriesView(ListModelMixin, BaseView):
    serializer_classes = {'get': TagsCategoriesSerializer}
    queryset = Category.objects.prefetch_related('tag_set').all()
    
    def get(self, request):
        return self.list(request)
