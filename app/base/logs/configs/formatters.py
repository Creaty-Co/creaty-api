__all__ = ['web', 'api']

from django.conf import settings

_datefmt = '[%d.%m%y-%H:%M:%S]'
_class = 'app.base.logs.formatters.ErrorFormatter'

web = {
    '__name__': 'web_formatter',
    'class': _class,
    'datefmt': _datefmt,
    'format': settings.LOG_FORMATTERS.get('web'),
}

api = {
    '__name__': 'api_formatter',
    'class': _class,
    'datefmt': _datefmt,
    'format': settings.LOG_FORMATTERS.get('api'),
}
