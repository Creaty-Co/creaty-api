from rest_framework.mixins import CreateModelMixin

from admin_.views import BaseAdminView
from tags.models import Category
from tags.serializers.categories.tags import TagsCategoryTagsSerializer


class TagsCategoryTagsView(CreateModelMixin, BaseAdminView):
    lookup_url_kwarg = 'category_id'
    serializer_classes = {'post': TagsCategoryTagsSerializer}
    queryset = Category.objects.all()
    
    def post(self, request, **_):
        return self.create(request)
    
    def perform_create(self, serializer):
        serializer.save(category=self.get_object())
