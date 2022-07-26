from rest_framework.mixins import UpdateModelMixin

from admin_.views import BaseAdminView
from forms.models import Form
from forms.serializers.detail import FormSerializer


class FormView(UpdateModelMixin, BaseAdminView):
    serializer_classes = {'patch': FormSerializer}
    queryset = Form.objects.all()

    def patch(self, request, **_):
        return self.partial_update(request)
