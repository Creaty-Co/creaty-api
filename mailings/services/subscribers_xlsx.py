import tablib
from django.http import HttpResponse

from mailings.models import Subscriber


class SubscribersXlsxConverter:
    FIELD_HEADER_MAP = {'id': 'Id', 'email': 'Email'}
    CONTENT_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    
    def __init__(self, field_header_map: dict[str, str] = None):
        if field_header_map is None:
            field_header_map = self.FIELD_HEADER_MAP
        self.fields = list(field_header_map.keys())
        self.headers = list(field_header_map.values())
    
    def to_xlsx_response(self):
        data = tablib.Dataset(headers=self.headers)
        subscribers = Subscriber.objects.values_list(*self.fields)
        for subscriber in subscribers:
            data.append(subscriber)
        response = HttpResponse(data.export('xlsx'), content_type=self.CONTENT_TYPE)
        response['Content-Disposition'] = 'attachment; filename=subscribers.xlsx'
        return response
