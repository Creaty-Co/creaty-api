from rest_framework.mixins import CreateModelMixin

from base.views.base import BaseView
from tags.models import Category
from tags.serializers.categories.tags import TagsCategoryTagsSerializer


class TagsCategoryTagsView(CreateModelMixin, BaseView):
    lookup_url_kwarg = 'category_id'
    serializer_classes = {'post': TagsCategoryTagsSerializer}
    queryset = Category.objects.all()
    
    def post(self, request):
        return self.create(request)
    
    def perform_create(self, serializer):
        serializer.save(category=self.get_object())
