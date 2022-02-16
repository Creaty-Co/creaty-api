from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin

from admin_.views import BaseAdminView
from tags.models import Tag
from tags.serializers.detail import UpdateTagSerializer


class TagView(UpdateModelMixin, DestroyModelMixin, BaseAdminView):
    serializer_classes = {'patch': UpdateTagSerializer}
    queryset = Tag.objects.all()
    
    def patch(self, request, **_):
        return self.partial_update(request)
    
    def delete(self, request, **_):
        return self.destroy(request)
