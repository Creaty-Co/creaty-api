import tablib
from django.http import HttpResponse

from mailings.models import Subscriber


class SubscribersXlsxConverter:
    FIELD_HEADER_MAP = {'id': 'Id', 'email': 'Email'}
    
    def __init__(self, field_header_map: dict[str, str]):
        self.fields = list(field_header_map.keys())
        self.headers = list(field_header_map.keys())
    
    def to_xlsx_response(self):
        data = tablib.Dataset(headers=self.headers)
        subscribers = Subscriber.objects.values(*self.fields)
        for subscriber in subscribers:
            data.append((subscriber, subscriber))
        response = HttpResponse(data.export('xlsx'), content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename=export.xls'
        return response
