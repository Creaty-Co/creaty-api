from app.admin_.permissions import AdminPermission
from app.base.utils.common import response_204
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

    @response_204
    def patch(self):
        self.update()
