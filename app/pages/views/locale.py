from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response

from app.admin_.permissions import AdminPermission
from app.base.utils.common import response_204
from app.base.utils.schema import schema_serializer
from app.base.views import BaseView
from app.pages.models import Locale


class PagesLocaleView(BaseView):
    queryset = Locale.objects.all()
    lookup_field = 'language'
    serializer_class = schema_serializer('PagesLocale', key=serializers.JSONField())
    permissions_map = {'put': [AdminPermission]}

    def get(self):
        return Response(self.get_object().json)

    @response_204
    def put(self, request, **_):
        locale = self.get_object()
        locale.json = request.data
        locale.save()

    def get_object(self) -> Locale:
        try:
            return super().get_object()  # noqa
        except Http404:
            if self.request.method.lower() == 'put':
                return Locale(language=self.kwargs['language'])
            raise
