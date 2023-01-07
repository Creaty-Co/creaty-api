from app.admin_.permissions import AdminPermission
from app.pages.serializers.main import (
    PagesRetrieveMainSerializer,
    PagesUpdateMainSerializer,
)
from app.pages.views.base import BaseMainPageView


class PagesMainView(BaseMainPageView):
    serializer_map = {
        'get': PagesRetrieveMainSerializer,
        'patch': PagesUpdateMainSerializer,
    }
    permissions_map = {'patch': [AdminPermission]}

    def get(self):
        return self.retrieve()

    def patch(self):
        return self.update()
