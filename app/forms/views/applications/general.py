from rest_framework.generics import get_object_or_404

from app.base.utils.common import response_204
from app.base.views.base import BaseView
from app.forms.models import Form
from app.forms.serializers.applications.general import FormApplicationsSerializer


class FormApplicationsView(BaseView):
    serializer_map = {'post': FormApplicationsSerializer}

    @response_204
    def post(self):
        self.create(form=get_object_or_404(Form, id=self.kwargs['form_id']))
