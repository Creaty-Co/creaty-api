import json
import logging

from django.db.models.sql.compiler import SQLCompiler
from silk.collector import DataCollector
from silk.config import SilkyConfig
from silk.middleware import SilkyMiddleware as _SilkyMiddleware
from silk.model_factory import DefaultEncoder
from silk.model_factory import RequestModelFactory as _RequestModelFactory
from silk.sql import execute_sql

# noinspection PyProtectedMember
from silk.middleware import _should_intercept  # isort:skip


class RequestModelFactory(_RequestModelFactory):
    def encoded_headers(self):
        headers = {}
        for k, v in self.request.META.items():
            if k.startswith('HTTP') or k in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                splt = k.split('_')
                if splt[0] == 'HTTP':
                    splt = splt[1:]
                k = '-'.join(splt)
                headers[k] = v
        if SilkyConfig().SILKY_HIDE_COOKIES:
            try:
                del headers['COOKIE']
            except KeyError:
                pass
        return json.dumps(
            headers,
            cls=DefaultEncoder,
            ensure_ascii=SilkyConfig().SILKY_JSON_ENSURE_ASCII,
        )


class SilkyMiddleware(_SilkyMiddleware):
    def process_request(self, request):
        DataCollector().clear()
        if not _should_intercept(request):
            return
        logging.getLogger('silk.middleware').debug('process_request')
        request.silk_is_intercepted = True
        self._apply_dynamic_mappings()
        if not hasattr(SQLCompiler, '_execute_sql'):
            SQLCompiler._execute_sql = SQLCompiler.execute_sql
            SQLCompiler.execute_sql = execute_sql
        silky_config = SilkyConfig()
        should_profile = silky_config.SILKY_PYTHON_PROFILER
        if silky_config.SILKY_PYTHON_PROFILER_FUNC:
            should_profile = silky_config.SILKY_PYTHON_PROFILER_FUNC(request)
        request_model = RequestModelFactory(request).construct_request_model()
        DataCollector().configure(request_model, should_profile=should_profile)
