from rest_framework.response import Response

from app.base.views import BaseView
from app.users.serializers.register.general import POSTUsersRegisterSerializer
from app.users.verification import register_verifier


class UsersRegisterView(BaseView):
    serializer_map = {'post': POSTUsersRegisterSerializer}

    def post(self):
        serializer = self.get_valid_serializer()
        user = serializer.save()
        register_verifier.send(user.email)
        return Response(serializer.data, 201)
