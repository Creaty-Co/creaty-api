from app.admin_.permissions import AdminPermission
from app.base.views import BaseView
from app.mailings.models import Mailing
from app.mailings.serializers.detail import MailingSerializer


class MailingView(BaseView):
    serializer_map = {'get': MailingSerializer}
    permissions_map = {'get': [AdminPermission]}
    queryset = Mailing.objects.all()

    def get(self):
        return self.retrieve()
