from rest_framework.throttling import AnonRateThrottle

from app.base.utils.common import response_204
from app.base.views.base import BaseView
from app.users.models import User
from app.users.serializers.register.resend import POSTUsersRegisterResendSerializer
from app.users.verification import register_verifier


class UsersRegisterResendView(BaseView):
    serializer_map = {'post': POSTUsersRegisterResendSerializer}
    throttle_map = {'post': [(AnonRateThrottle, ['30/s', '10/d'])]}

    @response_204
    def post(self):
        serializer = self.get_valid_serializer()
        if not User.objects.filter(email=serializer.validated_data['email']).exists():
            raise serializer.WARNINGS[404]
        register_verifier.send(serializer.validated_data['email'])
