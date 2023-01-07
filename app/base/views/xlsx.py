from django.utils.crypto import get_random_string
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers, status
from rest_framework.response import Response

from app.admin_.permissions import AdminPermission
from app.base.exceptions import ClientError
from app.base.services.cache import BaseCacheService
from app.base.services.xlsx import BaseXlsxConverter
from app.base.utils.common import add_query_params, response_204
from app.base.utils.schema import schema_serializer
from app.base.views.base import BaseView


class _XlsxCacheService(BaseCacheService):
    SCOPE = 'xlsx'


class BaseXlsxView(BaseView):
    xlsx_converter: BaseXlsxConverter
    cache_service: BaseCacheService = _XlsxCacheService()

    serializer_map = {
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
    permissions_map = {'post': [AdminPermission], 'put': [AdminPermission]}

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

    @response_204
    def put(self, request):
        try:
            self.xlsx_converter.parse(request.FILES['xlsx'])
        except KeyError:
            raise ClientError('В форме нет файла с ключом xlsx')
