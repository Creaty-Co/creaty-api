from rest_framework.response import Response

from app.base.views import BaseView
from app.calcom.serializers.token import GET_CalcomTokenSerializer
from app.calcom.services.auth import CalAuthService
from app.users.permissions import AuthenticatedPermission


class CalcomTokenView(BaseView):
    permissions_map = {'get': [AuthenticatedPermission]}
    serializer_map = {'get': GET_CalcomTokenSerializer}

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
