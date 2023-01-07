from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination as _PageNumberPagination
from rest_framework.response import Response

from app.base.paginations.mixin import BasePaginationMixin


class PageNumberPagination(BasePaginationMixin, _PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            OrderedDict([('count', self.page.paginator.count), ('results', data)])
        )
