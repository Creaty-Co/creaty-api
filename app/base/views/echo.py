from django.utils.html import escape
from rest_framework.response import Response

from app.base.views.base import BaseView

__all__ = ['EchoView']


# noinspection PyMethodMayBeStatic
class EchoView(BaseView):
    def get(self, request, *args, **kwargs):
        return Response(
            {
                'data': escape(str(request.data)),
                'query_params': escape(str(request.query_params)),
                'files': escape(str(request.FILES)),
            }
        )

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
