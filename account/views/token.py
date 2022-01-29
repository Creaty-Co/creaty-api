from rest_framework import status
from rest_framework.response import Response

from app.accounts.permissions import IsAuthenticatedPermission
from app.accounts.serializers.token import AccountsTokenSerializer
from app.accounts.services.auth import AuthService
from app.main.views.base import BaseView


# noinspection PyMethodMayBeStatic
class AccountsTokenView(BaseView):
    serializer_classes = {'post': AccountsTokenSerializer}
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        AuthService(request).logout()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_permissions(self):
        if self.request.method.lower() == 'delete':
            return [IsAuthenticatedPermission()]
        return []
