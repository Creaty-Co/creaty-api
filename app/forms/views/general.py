from app.base.views import BaseView
from app.forms.filters.general import FormsFilterSet
from app.forms.models import Form
from app.forms.serializers.general import FormsSerializer


class FormsView(BaseView):
    many = True
    serializer_map = {'get': FormsSerializer}
    queryset = Form.objects.all()
    filterset_class = FormsFilterSet

    def get(self):
        return self.list()
