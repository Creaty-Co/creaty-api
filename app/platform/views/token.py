from app.base.utils.common import response_204
from app.base.views import BaseView
from app.platform.services.auth import PlatformAuthService
from app.users.permissions import AuthenticatedPermission


class PlatformTokenView(BaseView):
    permissions_map = {'get': [AuthenticatedPermission]}

    @response_204
    def get(self):
        user = self.request.user
        platform_auth_service = PlatformAuthService()
        try:
            token = platform_auth_service.token(user)
        except platform_auth_service.PlatformAuthError:
            platform_auth_service.register(user)
            token = platform_auth_service.token(user)
        return platform_auth_service.set_cookie(token)
