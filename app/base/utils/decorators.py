from django.dispatch import receiver as _receiver
from drf_spectacular.utils import OpenApiResponse, extend_schema


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
