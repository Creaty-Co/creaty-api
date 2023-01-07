from collections import OrderedDict

from rest_framework.pagination import LimitOffsetPagination as _LimitOffsetPagination
from rest_framework.response import Response

from app.base.paginations.mixin import BasePaginationMixin


class LimitOffsetPagination(BasePaginationMixin, _LimitOffsetPagination):
    max_limit = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([('count', self.count), ('results', data)]))
