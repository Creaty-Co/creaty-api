from app.admin_.permissions import AdminPermission
from app.base.utils.common import response_204
from app.base.views import BaseView
from app.forms.models import Form
from app.forms.serializers.detail import FormSerializer


class FormView(BaseView):
    serializer_map = {'patch': FormSerializer}
    permissions_map = {'patch': [AdminPermission]}
    queryset = Form.objects.all()

    @response_204
    def patch(self):
        self.update()
