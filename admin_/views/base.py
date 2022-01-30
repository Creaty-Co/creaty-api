from account.views import BaseAuthView
from admin_.permissions import IsAdminPermission


class BaseAdminView(BaseAuthView):
    permission_classes = BaseAuthView.permission_classes + [IsAdminPermission]
