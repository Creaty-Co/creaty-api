from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin

from base.views.base import BaseView
from tags.models import Category
from tags.serializers.categories.detail import TagsCategorySerializer


class TagsCategoryView(UpdateModelMixin, DestroyModelMixin, BaseView):
    serializer_classes = {'get': TagsCategorySerializer}
    queryset = Category.objects.all()
    
    def patch(self, request, **_):
        return self.partial_update(request)
    
    def destroy(self, request, **_):
        return self.destroy(request)
