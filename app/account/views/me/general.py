from app.account.permissions import AuthenticatedPermission
from app.account.serializers.me.general import (
    GET_AccountMeSerializer,
    PATCH_AccountMeSerializer,
)
from app.base.utils.common import response_204
from app.base.views.base import BaseView


class AccountMeView(BaseView):
    permissions_map = {
        'get': [AuthenticatedPermission],
        'patch': [AuthenticatedPermission],
    }
    serializer_map = {
        'get': GET_AccountMeSerializer,
        'patch': PATCH_AccountMeSerializer,
    }

    def get(self):
        return self.retrieve()

    @response_204
    def patch(self):
        self.update()

    def get_object(self):
        return self.request.user
