from app.admin_.permissions import AdminPermission
from app.base.utils.common import response_204
from app.pages.serializers.main import (
    PagesRetrieveMainSerializer,
    PagesUpdateMainSerializer,
)
from app.pages.views.base import BasePageView


class PagesMainView(BasePageView):
    serializer_map = {
        'get': PagesRetrieveMainSerializer,
        'patch': PagesUpdateMainSerializer,
    }
    permissions_map = {'patch': [AdminPermission]}

    def get(self):
        return self.retrieve()

    @response_204
    def patch(self):
        self.update()
