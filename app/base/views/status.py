from rest_framework.response import Response

from app.base.views.base import BaseView


class StatusView(BaseView):
    def get(self):
        return Response({'status': 'ok'}, status=200)
