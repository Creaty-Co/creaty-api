from app.base.services.xlsx import BaseXlsxConverter
from app.mailings.models import Subscriber


class SubscribersXlsxConverter(BaseXlsxConverter):
    MODEL = Subscriber
    FIELD_HEADER_MAP = {'id': 'Id', 'email': 'Email'}

    def __init__(self):
        super().__init__(self.FIELD_HEADER_MAP)
