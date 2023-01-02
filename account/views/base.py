from drf_spectacular.utils import extend_schema
from rest_framework.throttling import UserRateThrottle

from account.authentications.token import TokenAuthentication
from account.permissions import IsAuthenticatedPermission
from base.views.base import BaseView

__all__ = ['BaseAuthView']


class BaseAuthView(BaseView):
    permission_classes = BaseView.permission_classes + [IsAuthenticatedPermission]
    throttle_classes = BaseView.throttle_classes + [UserRateThrottle]

    @classmethod
    def _to_auth_schema(cls, class_) -> None:
        auth_schema = TokenAuthentication.WARNING_401.to_schema()
        for method_name in class_.http_method_names:
            try:
                method = getattr(class_, method_name)
            except AttributeError:
                continue
            setattr(
                class_, method_name, extend_schema(responses={401: auth_schema})(method)
            )

    @classmethod
    def _to_schema(cls, class_) -> None:
        cls._to_auth_schema(class_)
        super()._to_schema(class_)
