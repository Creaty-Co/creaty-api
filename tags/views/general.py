from rest_framework.mixins import CreateModelMixin, ListModelMixin

from base.views.base import BaseView
from tags.models import Tag
from tags.serializers.general import ListTagsSerializer


class TagsView(ListModelMixin, CreateModelMixin, BaseView):
    serializer_classes = {'get': ListTagsSerializer}
    queryset = Tag.objects.all()
    
    def get(self, request):
        return self.list(request)
