from rest_framework.exceptions import APIException, ErrorDetail

from base.exceptions import ClientError
from base.exceptions.warning import APIWarning


def extract_detail(api_exception: APIException):
    def _extract_detail(detail):
        if isinstance(detail, dict):
            if isinstance(error_detail := detail.get('message'), ErrorDetail):
                detail['message'] = str(error_detail)
            else:
                for k, v in detail.items():
                    detail[k] = _extract_detail(v)
        elif isinstance(detail, list):
            return [_extract_detail(d) for d in detail]
        return detail
    
    return _extract_detail(api_exception.get_full_details())


def warning_cast_rest_api_exception(exception: APIException):
    codes = list(exception.get_codes())
    return APIWarning(
        codes[0] if codes else None, extract_detail(exception),
        getattr(exception, 'status_code')
    )


def client_error_cast_rest_api_exception(exception: APIException):
    codes = list(exception.get_codes())
    return ClientError(
        extract_detail(exception), getattr(exception, 'status_code'),
        codes[0] if codes else None
    )
