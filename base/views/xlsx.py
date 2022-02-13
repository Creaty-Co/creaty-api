from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from base.exceptions import ClientError
from base.services.xlsx import BaseXlsxConverter
from base.utils.decorators import schema_response_204
from base.utils.functions import schema_serializer
from base.views.base import BaseView


class BaseXlsxView(BaseView):
    xlsx_converter: BaseXlsxConverter
    
    serializer_classes = {
        'put': extend_schema_serializer(
            examples=[OpenApiExample('XlsxExample', {'xlsx': 'file.xlsx'})]
        )(schema_serializer('XlsxSerializer', xlsx=serializers.CharField()))
    }
    
    def get(self, request):
        return self.xlsx_converter.to_response()
    
    @schema_response_204
    def put(self, request):
        try:
            self.xlsx_converter.parse(request.FILES['xlsx'])
        except KeyError:
            raise ClientError('В форме нет файла с ключом xlsx')
