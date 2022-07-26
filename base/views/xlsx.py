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
from base.views import BaseView


class _XlsxCacheService(BaseCacheService):
    SCOPE = 'xlsx'


class BaseXlsxView(BaseView):
    xlsx_converter: BaseXlsxConverter
    cache_service: BaseCacheService = _XlsxCacheService()

    serializer_classes = {
        'post': schema_serializer(
            'CreateXlsxSerializer', link=serializers.CharField(read_only=True)
        ),
        'put': extend_schema_serializer(
            examples=[OpenApiExample('UpdateXlsxExample', {'xlsx': 'file.xlsx'})]
        )(
            schema_serializer(
                'UpdateXlsxSerializer', xlsx=serializers.CharField(write_only=True)
            )
        ),
    }
    permission_classes_map = {
        'post': BaseAdminView.permission_classes,
        'put': BaseAdminView.permission_classes,
    }

    def post(self, request):
        session_id = get_random_string(10)
        self.cache_service.set(session_id, 'session_id', timeout=30)
        return Response(
            {
                'link': add_query_params(
                    request.build_absolute_uri(), session_id=session_id
                )
            }
        )

    def get(self, request):
        if session_id := request.query_params.get('session_id'):
            if self.cache_service.get('session_id') == session_id:
                self.cache_service.delete('session_id')
                return self.xlsx_converter.to_response()
        return Response(status=status.HTTP_403_FORBIDDEN)

    @schema_response_204
    def put(self, request):
        try:
            self.xlsx_converter.parse(request.FILES['xlsx'])
        except KeyError:
            raise ClientError('В форме нет файла с ключом xlsx')
