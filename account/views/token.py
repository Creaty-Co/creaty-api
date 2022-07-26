from rest_framework import status
from rest_framework.response import Response

from account.permissions import IsAuthenticatedPermission
from account.serializers.token import AccountsTokenSerializer
from account.services.auth import AuthService
from base.views.base import BaseView


# noinspection PyMethodMayBeStatic
class AccountsTokenView(BaseView):
    serializer_classes = {'post': AccountsTokenSerializer}
    permission_classes_map = {'delete': [IsAuthenticatedPermission]}

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        AuthService(request).logout()
        return Response(status=status.HTTP_204_NO_CONTENT)
