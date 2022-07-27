from django.http import Http404
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin

from admin_.views import BaseAdminView
from base.utils.decorators import schema_response_204
from pages.models import Locale
from pages.serializers.locale import PagesLocaleSerializer


class PagesLocaleView(RetrieveModelMixin, UpdateModelMixin, BaseAdminView):
    queryset = Locale.objects.all()
    lookup_field = 'language'
    serializer_classes = {'get': PagesLocaleSerializer, 'put': PagesLocaleSerializer}

    def get(self, request, **_):
        return self.retrieve(request)

    @schema_response_204
    def put(self, request, **_):
        self.update(request)

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            if self.request.method.lower() == 'put':
                return Locale(language=self.kwargs['language'])
            raise
