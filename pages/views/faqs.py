from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin

from admin_.views.base import BaseAdminView
from base.views.base import BaseView
from pages.models import Faq
from pages.serializers.faqs import (
    CreatePagesFaqsSerializer, ListPagesFaqsSerializer, PagesFaqSerializer
)


class PagesFaqsView(ListModelMixin, CreateModelMixin, BaseView):
    serializer_classes = {
        'get': ListPagesFaqsSerializer, 'post': CreatePagesFaqsSerializer
    }
    permission_classes_map = {'post': BaseAdminView.permission_classes}
    queryset = Faq.objects.all()
    
    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)


class PagesFaqView(UpdateModelMixin, BaseView):
    serializer_classes = {'patch': PagesFaqSerializer}
    queryset = Faq.objects.all()
    
    def patch(self, request, **_):
        return self.partial_update(request)
