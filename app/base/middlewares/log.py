# taken from https://gist.github.com/SehgalDivij/1ca5c647c710a2c3a0397bce5ec1c1b4

"""
Middleware to log all requests and responses.
Uses a logger_config configured by the name of django.request
to log all requests and responses according to configuration
specified for django.request.
"""

import json
import time
from typing import Iterable, Sized
from urllib.parse import unquote

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

from app.base.logs import debug, info

__all__ = ['LogMiddleware']


def _get_content_type(request_or_response):
    return getattr(request_or_response, 'content_type', None) or getattr(
        request_or_response, 'headers', {}
    ).get("Content-Type", '')


# noinspection PyBroadException
def _cut_back(value, max_length=200):
    if isinstance(value, dict):
        value = _cut_back_dict(value)
    if isinstance(value, Sized):
        length = len(value)
        if length > max_length:
            type_name = type(value).__name__
            try:
                return (
                    f"{value[:max_length // 2]}<<<{length - max_length} more "
                    f"{type_name}>>> {value[-max_length // 2:]}"
                )
            except Exception:
                return f"<<<{type_name} of length {length}>>>"
        return value
    if len(str(value)) > max_length:
        return _cut_back(str(value))
    return value


def _cut_back_dict(json_data, max_length=200):
    json_data = json.loads(json.dumps(json_data))
    for k, v in json_data.items():
        if isinstance(v, dict):
            v = _cut_back_dict(v, max_length)
        elif not isinstance(v, (str, bytes, bytearray)) and isinstance(v, Iterable):
            v = [_cut_back(e, max_length) for e in v]
        else:
            v = _cut_back(v, max_length)
        json_data[k] = v
    return json_data


# noinspection PyMethodMayBeStatic, PyBroadException
class LogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
        request.body_ = request.body

    def extract_log_info(self, request, response):
        log_data = {
            'run_time': time.time() - request.start_time,
            'request': {},
            'response': {},
            'url': f"{request.method.upper()} {unquote(request.get_full_path())}",
        }

        log_data['request']['headers'] = _cut_back_dict(dict(request.headers))
        log_data['request']['cookies'] = _cut_back_dict(dict(request.COOKIES))
        if request.method in ['PUT', 'POST', 'PATCH']:
            try:
                log_data['request']['data'] = _cut_back_dict(json.loads(request.body_))
            except Exception:
                log_data['request']['data'] = _cut_back(request.body_)
            try:
                log_data['request']['files'] = {
                    k: [e.name for e in f] for k, f in dict(request.FILES).items()
                }
            except Exception:
                log_data['request']['files'] = {}
            if not log_data['request']['files']:
                del log_data['request']['files']

        if response:
            log_data['response']['headers'] = _cut_back_dict(dict(response.headers))
            log_data['response']['cookies'] = _cut_back_dict(dict(response.cookies))
            content_type = _get_content_type(response)
            if request.path in ('/', '/__docs__/'):
                log_data['response']['body'] = "<<<DOCS>>>"
                return log_data
            if request.path.startswith('/__debug__'):
                log_data['response']['body'] = "<<<DEBUG TOOLBAR>>>"
                return log_data
            if 'text/html' in content_type and len(response.content) > 100:
                log_data['response']['body'] = "<<<HTML>>>"
                return log_data
            if 'application/json' in content_type:
                try:
                    log_data['response']['data'] = _cut_back_dict(dict(response.data))
                    return log_data
                except Exception:
                    pass
            if hasattr(response, 'content'):
                try:
                    log_data['response']['data'] = _cut_back_dict(
                        dict(response.content)
                    )
                except Exception:
                    log_data['response']['data'] = _cut_back(response.content)
        return log_data

    def process_response(self, request, response):
        if settings.LOG_REQUESTS:
            self.log(request, response)
        return response

    def log(self, request, response):
        log_data = self.extract_log_info(request=request, response=response)
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            info(log_data)
        else:
            debug(log_data)
