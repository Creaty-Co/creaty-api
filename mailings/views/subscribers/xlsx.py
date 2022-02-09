from base.views.base import BaseView
from mailings.services.subscribers_xlsx import SubscribersXlsxConverter


class MailingsSubscribersXlsxView(BaseView):
    def get(self, request):
        return SubscribersXlsxConverter().to_xlsx_response()
