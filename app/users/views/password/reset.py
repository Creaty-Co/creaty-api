from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from drf_spectacular.utils import OpenApiResponse, extend_schema

from app.base.utils.common import response_204
from app.base.views import BaseView
from app.users.password_reset import password_resetter
from app.users.verification import register_verifier


class UsersPasswordResetView(BaseView):
    # serializer_map = {'post': (204, POSTUsersPasswordResetSerializer)}  TODO

    @extend_schema(
        responses={
            200: None,
            302: OpenApiResponse(
                description=(
                    f"redirect:"
                    f"\n\n{'&nbsp;' * 4}failure url: {password_resetter.failure_url}"
                    f"\n\n{'&nbsp;' * 4}successful url: "
                    f"{password_resetter.successful_url}"
                )
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        email, session_id = request.query_params.get('email'), request.query_params.get(
            'session_id'
        )
        if email is not None and session_id is not None:
            if password_resetter.verifier.check(email, session_id):
                return HttpResponseRedirect(password_resetter.successful_url)
        return HttpResponseRedirect(password_resetter.failure_url)

    @response_204
    def post(self):
        serializer = self.get_valid_serializer()
        valid_data = serializer.validated_data
        valid_data['password'] = make_password(valid_data['password'])
        register_verifier.send(valid_data['email'], valid_data)

    @response_204
    def put(self):
        pass  # TODO
