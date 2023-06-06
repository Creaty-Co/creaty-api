from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from app.base.views import BaseView
from app.users.regisration import registerer
from app.users.serializers.register.general import (
    POSTUsersRegisterSerializer,
    PUTUsersRegisterSerializer,
)
from app.users.verification import register_verifier


class UsersRegisterView(BaseView):
    serializer_map = {
        'post': POSTUsersRegisterSerializer,
        'put': (200, PUTUsersRegisterSerializer),
    }

    def post(self):
        serializer = self.get_valid_serializer()
        user = serializer.save()
        token: RefreshToken = RefreshToken.for_user(user)
        user.access = str(token.access_token)
        user.refresh = str(token)
        register_verifier.send(user.email)
        return Response(serializer.data, 201)

    def put(self):
        serializer = self.get_valid_serializer()
        code = serializer.validated_data['code']
        try:
            user = registerer.register(code)
        except registerer.InvalidCodeError as exc:
            raise serializer.WARNINGS[408] from exc
        token: RefreshToken = RefreshToken.for_user(user)
        serializer.instance = {'access': str(token.access_token), 'refresh': str(token)}
        return Response(serializer.data)
