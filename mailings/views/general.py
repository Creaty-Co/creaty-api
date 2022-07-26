from rest_framework.mixins import CreateModelMixin, ListModelMixin

from admin_.views.base import BaseAdminView
from mailings.models import Mailing
from mailings.serializers.general import (
    MailingsCreateSerializer,
    MailingsListSerializer,
)


class MailingsView(ListModelMixin, CreateModelMixin, BaseAdminView):
    serializer_classes = {
        'get': MailingsListSerializer,
        'post': MailingsCreateSerializer,
    }
    queryset = Mailing.objects.all()

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)
