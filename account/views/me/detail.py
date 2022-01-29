from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin

from account.serializers.me.detail import AccountsMeSerializer
from account.views.base import BaseAuthView


class AccountsMeView(RetrieveModelMixin, UpdateModelMixin, BaseAuthView):
    serializer_classes = {
        'get': AccountsMeSerializer, 'patch': AccountsMeSerializer
    }
    
    def get(self, request):
        return self.retrieve(request)
    
    def patch(self, request):
        return self.partial_update(request)
    
    def get_object(self):
        return self.request.user
