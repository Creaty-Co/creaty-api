from rest_framework.authentication import get_authorization_header

from app.base.exceptions import ClientError


def get_header(request):
    header = get_authorization_header(request)
    if header == b'':
        return None
    try:
        return header.decode()
    except UnicodeError:
        raise ClientError('Неверная кодировка заголовка с токеном')
