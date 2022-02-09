from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin

from base.views.base import BaseView
from tags.models import Tag
from tags.serializers.detail import TagSerializer


class TagView(UpdateModelMixin, DestroyModelMixin, BaseView):
    serializer_classes = {'get': TagSerializer}
    queryset = Tag.objects.all()
    
    def patch(self, request, **_):
        return self.partial_update(request)
    
    def delete(self, request, **_):
        return self.destroy(request)
