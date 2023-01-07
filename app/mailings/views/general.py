from app.admin_.permissions import AdminPermission
from app.base.views import BaseView
from app.mailings.models import Mailing
from app.mailings.serializers.general import (
    MailingsCreateSerializer,
    MailingsListSerializer,
)


class MailingsView(BaseView):
    many = True
    serializer_map = {
        'get': MailingsListSerializer,
        'post': MailingsCreateSerializer,
    }
    permissions_map = {'get': [AdminPermission], 'post': [AdminPermission]}
    queryset = Mailing.objects.all()

    def get(self):
        return self.list()

    def post(self):
        return self.create()
