from app.admin_.permissions import AdminPermission
from app.base.utils.common import response_204
from app.base.views import BaseView
from app.pages.models import DocumentLink
from app.pages.serializers.links.documents import (
    ListPagesLinksDocumentsSerializer,
    PagesLinksDocumentSerializer,
)


class PagesLinksDocumentsView(BaseView):
    many = True
    serializer_map = {'get': ListPagesLinksDocumentsSerializer}
    queryset = DocumentLink.objects.all()

    def get(self):
        return self.list()


class PagesLinksDocumentView(BaseView):
    serializer_map = {'patch': PagesLinksDocumentSerializer}
    permissions_map = {'patch': [AdminPermission]}
    queryset = DocumentLink.objects.all()

    @response_204
    def patch(self):
        self.update()
