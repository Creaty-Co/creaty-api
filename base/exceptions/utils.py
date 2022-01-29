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
