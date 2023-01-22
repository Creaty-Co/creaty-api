from app.admin_.permissions import AdminPermission
from app.base.utils.common import response_204
from app.base.views import BaseView
from app.pages.models import Faq
from app.pages.serializers.faqs import (
    CreatePagesFaqsSerializer,
    ListPagesFaqsSerializer,
    PagesFaqSerializer,
)


class PagesFaqsView(BaseView):
    many = True
    serializer_map = {
        'get': ListPagesFaqsSerializer,
        'post': CreatePagesFaqsSerializer,
    }
    permissions_map = {'post': [AdminPermission]}
    queryset = Faq.objects.all()

    def get(self):
        return self.list()

    def post(self):
        return self.create()


class PagesFaqView(BaseView):
    serializer_map = {'patch': PagesFaqSerializer}
    permissions_map = {'patch': [AdminPermission], 'delete': [AdminPermission]}
    queryset = Faq.objects.all()

    @response_204
    def patch(self):
        self.update()

    def delete(self):
        return self.destroy()
