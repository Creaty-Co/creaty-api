from app.base.utils.common import response_204
from app.base.views import BaseView
from app.mailings.serializers.subscribe import MailingsSubscribeSerializer


class MailingsSubscribeView(BaseView):
    serializer_map = {'post': MailingsSubscribeSerializer}

    @response_204
    def post(self):
        self.create()
