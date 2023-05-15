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
        'put': (204, PUTUsersPasswordResetSerializer),
    }

    @response_204
    def post(self):
        serializer = self.get_valid_serializer()
        valid_data = serializer.validated_data
        password_reset_verifier.send(valid_data['email'])

    @response_204
    def put(self):
        serializer = self.get_valid_serializer()
        password_resetter.reset(**serializer.validated_data)
