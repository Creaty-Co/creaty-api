from django.http import HttpResponseRedirect
from rest_framework.response import Response

from app.base.views import BaseView
from app.users.regisration import registerer
from app.users.serializers.register.general import POSTUsersRegisterSerializer
from app.users.verification import register_verifier


class UsersRegisterView(BaseView):
    serializer_map = {'post': POSTUsersRegisterSerializer}

    def get(self, request, *args, **kwargs):
        email, code = request.query_params.get('email'), request.query_params.get(
            'code'
        )
        if email is not None and code is not None:
            if registerer.register(email, code):
                return HttpResponseRedirect(registerer.successful_url)
        return HttpResponseRedirect(registerer.failure_url)

    def post(self):
        serializer = self.get_valid_serializer()
        user = serializer.save()
        register_verifier.send(user.email)
        return Response(serializer.data, 201)
