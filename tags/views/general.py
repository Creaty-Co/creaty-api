from rest_framework.mixins import ListModelMixin

from base.views.base import BaseView
from tags.models import Tag
from tags.serializers.general import TagsSerializer


class TagsView(ListModelMixin, BaseView):
    serializer_classes = {'get': TagsSerializer}
    queryset = Tag.objects.all()
    
    def get(self, request):
        return self.list(request)
