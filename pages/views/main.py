from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin

from admin_.views.base import BaseAdminView
from pages.serializers.main import (
    PagesRetrieveMainSerializer,
    PagesUpdateMainSerializer,
)
from pages.views.base import BaseMainPageView


class PagesMainView(RetrieveModelMixin, UpdateModelMixin, BaseMainPageView):
    serializer_classes = {
    'get': PagesRetrieveMainSerializer,
    'patch': PagesUpdateMainSerializer,
}
    permission_classes_map = {'patch': BaseAdminView.permission_classes}

    def get(self, request):
        return self.retrieve(request)

    def patch(self, request):
        return self.partial_update(request)
