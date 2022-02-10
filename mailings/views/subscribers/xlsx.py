from base.views.xlsx import BaseXlsxView
from mailings.services.subscribers_xlsx import SubscribersXlsxConverter


class MailingsSubscribersXlsxView(BaseXlsxView):
    xlsx_converter = SubscribersXlsxConverter()
