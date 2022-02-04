from rest_framework.mixins import RetrieveModelMixin

from admin_.views.base import BaseAdminView
from mailings.models import Mailing
from mailings.serializers.detail import MailingSerializer


class MailingView(RetrieveModelMixin, BaseAdminView):
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()
    
    def get(self, request, **_):
        return self.retrieve(request)
