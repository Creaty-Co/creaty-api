from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin

from base.utils.decorators import schema_response_204
from base.views.base import BaseView
from forms.models import Form
from forms.serializers.applications.general import FormApplicationsSerializer


class FormApplicationsView(CreateModelMixin, BaseView):
    serializer_classes = {'post': FormApplicationsSerializer}

    @schema_response_204
    def post(self, request, **_):
        self.create(request)

    def perform_create(self, serializer):
        serializer.save(form=get_object_or_404(Form, id=self.kwargs['form_id']))
