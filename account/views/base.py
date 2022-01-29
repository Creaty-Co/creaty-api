from drf_spectacular.utils import extend_schema

from account.authentications.token import TokenAuthentication
from base.views.base import BaseView
from account.permissions import IsAuthenticatedPermission

__all__ = ['BaseAuthView']


class BaseAuthView(BaseView):
    permission_classes = [IsAuthenticatedPermission]
    
    @classmethod
    def _to_auth_schema(cls, clazz) -> None:
        auth_schema = TokenAuthentication.WARNING_401.to_schema()
        for method_name in clazz.http_method_names:
            try:
                method = getattr(clazz, method_name)
            except AttributeError:
                continue
            setattr(
                clazz, method_name, extend_schema(responses={401: auth_schema})(method)
            )
    
    @classmethod
    def _to_schema(cls, clazz) -> None:
        cls._to_auth_schema(clazz)
        super()._to_schema(clazz)
