from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from app.base.utils.common import response_204
from app.base.views import BaseView
from app.users.password_reset import password_resetter
from app.users.serializers.password.reset import (
    POSTUsersPasswordResetSerializer,
    PUTUsersPasswordResetSerializer,
)
from app.users.verification import password_reset_verifier


class UsersPasswordResetView(BaseView):
    serializer_map = {
        'post': (204, POSTUsersPasswordResetSerializer),
        'put': (200, PUTUsersPasswordResetSerializer),
    }
    throttle_map = {'post': [(AnonRateThrottle, ['2/m', '10/d'])]}

    @response_204
    def post(self):
        serializer = self.get_valid_serializer()
        password_reset_verifier.send(serializer.validated_data['email'])

    def put(self):
        serializer = self.get_valid_serializer()
        serializer.instance = password_resetter.reset(**serializer.validated_data)
        return Response(serializer.data)
