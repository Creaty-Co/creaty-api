from rest_framework.response import Response

from app.base.views import BaseView
from app.cal.serializers.token import GET_CalTokenSerializer
from app.cal.services.auth import CalAuthService
from app.users.permissions import AuthenticatedPermission


class CalTokenView(BaseView):
    permissions_map = {'get': [AuthenticatedPermission]}
    serializer_map = {'get': GET_CalTokenSerializer}

    def get(self):
        user = self.request.user
        cal_auth_service = CalAuthService()
        try:
            token = cal_auth_service.token(user)
        except cal_auth_service.CalAuthError:
            cal_auth_service.register(user)
            token = cal_auth_service.token(user)
        serializer = self.get_serializer(instance={'token': token})
        return Response(serializer.data)
