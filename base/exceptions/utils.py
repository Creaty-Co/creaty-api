from rest_framework.exceptions import APIException, ErrorDetail


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


def extract_first_code(api_exception: APIException):
    codes = api_exception.get_codes()
    if codes is None:
        return None
    if isinstance(codes, str):
        return codes
    if isinstance(codes, (list, tuple)):
        return codes[0]
    if isinstance(codes, dict):
        return list(codes.values())[0]
    return list(codes)[0]


def warning_cast_rest_api_exception(exception: APIException):
    from base.exceptions.warning import APIWarning
    code = extract_first_code(exception)
    return APIWarning(code, extract_detail(exception), getattr(exception, 'status_code'))


def client_error_cast_rest_api_exception(exception: APIException):
    from base.exceptions.client import ClientError
    code = extract_first_code(exception)
    return ClientError(extract_detail(exception), getattr(exception, 'status_code'), code)
