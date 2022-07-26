from rest_framework.mixins import ListModelMixin, UpdateModelMixin

from admin_.views.base import BaseAdminView
from base.views.base import BaseView
from pages.models import DocumentLink
from pages.serializers.links.documents import (
    ListPagesLinksDocumentsSerializer,
    PagesLinksDocumentSerializer,
)


class PagesLinksDocumentsView(ListModelMixin, BaseView):
    serializer_classes = {'get': ListPagesLinksDocumentsSerializer}
    queryset = DocumentLink.objects.all()

    def get(self, request):
        return self.list(request)


class PagesLinksDocumentView(UpdateModelMixin, BaseAdminView):
    serializer_classes = {'patch': PagesLinksDocumentSerializer}
    queryset = DocumentLink.objects.all()

    def patch(self, request, **_):
        return self.partial_update(request)
