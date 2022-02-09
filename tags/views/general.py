from rest_framework.mixins import CreateModelMixin, ListModelMixin

from base.views.base import BaseView
from tags.models import Tag
from tags.serializers.general import CreateTagsSerializer, ListTagsSerializer


class TagsView(ListModelMixin, CreateModelMixin, BaseView):
    serializer_classes = {'get': ListTagsSerializer, 'post': CreateTagsSerializer}
    queryset = Tag.objects.all()
    
    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)
