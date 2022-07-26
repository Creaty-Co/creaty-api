from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin

from admin_.views import BaseAdminView
from pages.serializers.persoanls.detail import (
    PagesRetrievePersonalSerializer,
    PagesUpdatePersonalSerializer,
)
from pages.views.peronals.base import BasePersonalPageView


class PagesPersonalView(RetrieveModelMixin, UpdateModelMixin, BasePersonalPageView):
    serializer_classes = {
        'get': PagesRetrievePersonalSerializer,
        'patch': PagesUpdatePersonalSerializer,
    }
    permission_classes_map = {'patch': BaseAdminView.permission_classes}

    def get(self, request, **_):
        return self.retrieve(request)

    def patch(self, request, **_):
        return self.partial_update(request)
