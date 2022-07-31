from django.http import Http404
from rest_framework import serializers
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin
from rest_framework.response import Response

from admin_.views import BaseAdminView
from base.utils.decorators import schema_response_204
from base.utils.functions import schema_serializer
from base.views import BaseView
from pages.models import Locale


class PagesLocaleView(RetrieveModelMixin, UpdateModelMixin, BaseView):
    queryset = Locale.objects.all()
    lookup_field = 'language'
    serializer_class = schema_serializer('PagesLocale', key=serializers.JSONField())
    permission_classes_map = {'get': (), 'put': BaseAdminView.permission_classes}

    def get(self, request, **_):
        return Response(self.get_object().json)

    @schema_response_204
    def put(self, request, **_):
        locale = self.get_object()
        locale.json = request.data
        locale.save()

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            if self.request.method.lower() == 'put':
                return Locale(language=self.kwargs['language'])
            raise
