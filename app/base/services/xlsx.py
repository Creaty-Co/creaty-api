from __future__ import annotations

from collections.abc import Iterable

import tablib
from django.http import HttpResponse

from app.base.models.base import BaseModel


class BaseXlsxConverter:
    MODEL: type[BaseModel]
    CONTENT_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    def __init__(self, field_header_map: dict[str, str], filename: str = None):
        self.fields = list(field_header_map.keys())
        self.headers = list(field_header_map.values())
        self.filename = filename or self.MODEL.__name__.lower()

    def _header_by_field(self, field):
        try:
            return self.headers[self.fields.index(field)]
        except ValueError:
            return field

    def _field_by_header(self, header):
        try:
            return self.fields[self.headers.index(header)]
        except ValueError:
            return header

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

    def parse(self, xlsx) -> None:
        instances_data = tablib.Dataset().load(xlsx, format='xlsx').dict
        instances_data = {
            inst_data.pop(self._header_by_field('id')): inst_data
            for inst_data in instances_data
        }
        self._update_objects(instances_data)

    def _update_objects(self, instances_data: dict) -> None:
        instances = self.MODEL.objects.filter(id__in=instances_data.keys())
        for instance in instances:
            for header, value in instances_data[instance.id].items():
                setattr(instance, self._field_by_header(header), value)
            instance.save()
