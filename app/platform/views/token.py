from rest_framework.response import Response

from app.base.views import BaseView
from app.platform.serializers.token import GET_PlatformTokenSerializer
from app.platform.services.auth import PlatformAuthService
from app.users.permissions import AuthenticatedPermission


class PlatformTokenView(BaseView):
    permissions_map = {'get': [AuthenticatedPermission]}
    serializer_map = {'get': GET_PlatformTokenSerializer}

    def get(self):
        user = self.request.user
        platform_auth_service = PlatformAuthService()
        try:
            token = platform_auth_service.token(user)
        except platform_auth_service.PlatformAuthError:
            platform_auth_service.register(user)
            token = platform_auth_service.token(user)
        serializer = self.get_serializer(instance={'token': token})
        return Response(serializer.data)
