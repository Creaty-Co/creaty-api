from django.conf import settings
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework.views import set_rollback

from .client import ClientError
from .critical import CriticalError
from .warning import APIWarning


def exception_handler(exception):
    try:
        if settings.DEBUG and isinstance(exception, MethodNotAllowed):
            return Response(str(exception.detail))
        try:
            raise exception
        except APIWarning as exc:
            api_error = exc
        except ClientError as exc:
            api_error = exc
        except CriticalError as exc:
            api_error = exc
        except tuple(APIWarning.EXCEPTION__CAST.keys()) as exception_to_cast:
            api_error = APIWarning.cast_exception(exception_to_cast)
        except tuple(ClientError.EXCEPTION__CAST.keys()) as exception_to_cast:
            api_error = ClientError.cast_exception(exception_to_cast)
        except tuple(CriticalError.EXCEPTION__CAST.keys()) as exception_to_cast:
            api_error = CriticalError.cast_exception(exception_to_cast)
            set_rollback()

        error = api_error

    except Exception as exc:
        error = CriticalError(str(exc))
        set_rollback()

    error.log()
    return error.to_response()
