from rest_framework.mixins import ListModelMixin

from base.views.base import BaseView
from forms.filters.general import FormsFilterSet
from forms.models import Form
from forms.serializers.general import FormsSerializer


class FormsView(ListModelMixin, BaseView):
    serializer_classes = {'get': FormsSerializer}
    queryset = Form.objects.all()
    filterset_class = FormsFilterSet
    
    def get(self, request):
        return self.list(request)
