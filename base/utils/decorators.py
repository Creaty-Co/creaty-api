from django.dispatch import receiver as _receiver
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.response import Response


def schema_response_204(f):
    def _f_decorator(*args, **kwargs):
        f(*args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)

    return extend_schema(responses={200: None, 201: None, 204: ''})(_f_decorator)


def schema_redirect(description: str = None):
    if description:
        response = OpenApiResponse(description=description)
    else:
        response = ''
    return extend_schema(responses={200: None, 302: response})


def receiver(signal, sender=None):
    def _decorator(f):
        return _receiver(signal, sender=sender, weak=False, dispatch_uid=f.__name__)(f)

    return _decorator
