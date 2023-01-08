from app.admin_.permissions import AdminPermission
from app.pages.serializers.persoanls.detail import (
    PagesRetrievePersonalSerializer,
    PagesUpdatePersonalSerializer,
)
from app.pages.views.peronals.base import BasePersonalPageView


class PagesPersonalView(BasePersonalPageView):
    serializer_map = {
        'get': PagesRetrievePersonalSerializer,
        'patch': PagesUpdatePersonalSerializer,
    }
    permissions_map = {'patch': [AdminPermission]}

    def get(self):
        return self.retrieve()

    def patch(self):
        return self.update()
