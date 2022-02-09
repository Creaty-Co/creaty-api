from typing import Iterable, Type

import tablib
from django.http import HttpResponse

from base.models import AbstractModel


class XlsxConverter:
    MODEL: Type[AbstractModel]
    CONTENT_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    
    def __init__(self, field_header_map: dict[str, str], filename: str = None):
        self.fields = list(field_header_map.keys())
        self.headers = list(field_header_map.values())
        self.filename = filename or self.MODEL.__name__.lower()
    
    def to_response(self):
        response = HttpResponse(self._to_xlsx(), content_type=self.CONTENT_TYPE)
        response['Content-Disposition'] = f'attachment; filename={self.filename}.xlsx'
        return response
    
    def _to_xlsx(self) -> bytes:
        data = tablib.Dataset(headers=self.headers)
        for value in self._get_values():
            data.append(value)
        return data.export('xlsx')
    
    def _get_values(self) -> Iterable:
        return self.MODEL.objects.values_list(*self.fields)
