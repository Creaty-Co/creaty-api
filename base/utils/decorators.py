from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response


def schema_response_204(f):
    def _f_decorator(*args, **kwargs):
        f(*args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    return extend_schema(responses={201: None, 204: ''})(_f_decorator)
