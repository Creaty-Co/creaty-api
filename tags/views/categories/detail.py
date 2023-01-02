from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin

from admin_.views import BaseAdminView
from tags.models import Category
from tags.serializers.categories.detail import TagsCategorySerializer


class TagsCategoryView(UpdateModelMixin, DestroyModelMixin, BaseAdminView):
    serializer_classes = {'patch': TagsCategorySerializer}
    queryset = Category.objects.all()

    def patch(self, request, **_):
        return self.partial_update(request)

    def delete(self, request, **_):
        return self.destroy(request)
