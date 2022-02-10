from base.serializers.xlsx import BaseXlsxSerializer
from base.services.xlsx import BaseXlsxConverter
from base.utils.decorators import schema_response_204
from base.views.base import BaseView


class BaseXlsxView(BaseView):
    xlsx_converter: BaseXlsxConverter
    
    serializer_classes = {'put': BaseXlsxSerializer}
    
    def get(self, request):
        return self.xlsx_converter.to_response()
    
    @schema_response_204
    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.xlsx_converter.parse(serializer.validated_data['xlsx'])
