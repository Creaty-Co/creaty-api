from app.base.views.xlsx import BaseXlsxView
from app.mailings.services.subscribers_xlsx import SubscribersXlsxConverter


class MailingsSubscribersXlsxView(BaseXlsxView):
    xlsx_converter = SubscribersXlsxConverter()
