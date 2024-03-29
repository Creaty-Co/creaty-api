from rest_framework.throttling import AnonRateThrottle

from app.base.utils.common import response_204
from app.base.views.base import BaseView
from app.users.models import User
from app.users.serializers.register.resend import POSTUsersRegisterResendSerializer
from app.users.verification import register_verifier


class UsersRegisterResendView(BaseView):
    serializer_map = {'post': POSTUsersRegisterResendSerializer}

    @response_204
    def post(self):
        serializer = self.get_valid_serializer()
        try:
            user = User.objects.get(email=serializer.validated_data['email'])
        except User.DoesNotExist as exc:
            raise serializer.WARNINGS[404] from exc
        if user.is_verified:
            raise serializer.WARNINGS[409]
        self.throttle_classes = []
        self.throttle_map = {'post': [(AnonRateThrottle, ['1/m', '10/d'])]}
        self.check_throttles(self.request)
        register_verifier.send(serializer.validated_data['email'])
