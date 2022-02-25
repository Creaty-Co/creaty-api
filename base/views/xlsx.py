from django.shortcuts import redirect
from django.utils.crypto import get_random_string
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers, status
from rest_framework.response import Response

from admin_.views import BaseAdminView
from base.exceptions import ClientError
from base.services.cache.cache import BaseCacheService
from base.services.xlsx import BaseXlsxConverter
from base.utils.decorators import schema_response_204
from base.utils.functions import add_query_params, schema_serializer


class _XlsxCacheService(BaseCacheService):
    SCOPE = 'xlsx'


class BaseXlsxView(BaseAdminView):
    xlsx_converter: BaseXlsxConverter
    cache_service: BaseCacheService = _XlsxCacheService()
    
    serializer_classes = {
        'put': extend_schema_serializer(
            examples=[OpenApiExample('XlsxExample', {'xlsx': 'file.xlsx'})]
        )(schema_serializer('XlsxSerializer', xlsx=serializers.CharField()))
    }
    
    def get(self, request):
        if session_id := request.query_params.get('session_id'):
            if self.cache_service.get('session_id') == session_id:
                self.cache_service.delete('session_id')
                return self.xlsx_converter.to_response()
            return Response(status=status.HTTP_403_FORBIDDEN)
        session_id = get_random_string(10)
        self.cache_service.set(session_id, 'session_id', timeout=30)
        return redirect(
            add_query_params(request.build_absolute_uri(), session_id=session_id)
        )
    
    @schema_response_204
    def put(self, request):
        try:
            self.xlsx_converter.parse(request.FILES['xlsx'])
        except KeyError:
            raise ClientError('В форме нет файла с ключом xlsx')
