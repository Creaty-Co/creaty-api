from rest_framework.mixins import UpdateModelMixin

from base.views.base import BaseView
from forms.models import Form
from forms.serializers.detail import FormSerializer


class FormView(UpdateModelMixin, BaseView):
    serializer_classes = {'patch': FormSerializer}
    queryset = Form.objects.all()
    
    def patch(self, request, **_):
        return self.partial_update(request)
