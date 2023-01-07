from app.admin_.permissions import AdminPermission
from app.base.views import BaseView
from app.forms.models import Form
from app.forms.serializers.detail import FormSerializer


class FormView(BaseView):
    serializer_map = {'patch': FormSerializer}
    permissions_map = {'patch': [AdminPermission]}
    queryset = Form.objects.all()

    def patch(self):
        return self.update()
