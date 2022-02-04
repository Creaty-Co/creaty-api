from rest_framework.mixins import CreateModelMixin

from base.utils.decorators import schema_response_204
from base.views.base import BaseView
from mailings.serializers.subscribe import MailingsSubscribeSerializer


class MailingsSubscribeView(CreateModelMixin, BaseView):
    serializer_classes = {'post': MailingsSubscribeSerializer}
    
    @schema_response_204
    def post(self, request):
        self.create(request)
