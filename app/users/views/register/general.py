from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from drf_spectacular.utils import OpenApiResponse, extend_schema

from app.base.utils.common import response_204
from app.base.views import BaseView
from app.users.regisration import registerer
from app.users.serializers.register.general import UsersRegisterSerializer
from app.users.verification import register_verifier


class UsersRegisterView(BaseView):
    serializer_map = {'post': (204, UsersRegisterSerializer)}

    @extend_schema(
        responses={
            200: None,
            302: OpenApiResponse(
                description=(
                    f"redirect:"
                    f"\n\n{'&nbsp;' * 4}failure url: {registerer.failure_url}"
                    f"\n\n{'&nbsp;' * 4}successful url: {registerer.successful_url}"
                )
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        email, code = request.query_params.get('email'), request.query_params.get(
            'code'
        )
        if email is not None and code is not None:
            if registerer.register(email, code):
                return HttpResponseRedirect(registerer.successful_url)
        return HttpResponseRedirect(registerer.failure_url)

    @response_204
    def post(self):
        serializer = self.get_valid_serializer(data=self.get_data())
        valid_data = serializer.validated_data
        valid_data['password'] = make_password(valid_data['password'])
        register_verifier.send(valid_data['email'], valid_data)
