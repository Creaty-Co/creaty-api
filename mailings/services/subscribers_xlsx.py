from base.services.xlsx import XlsxConverter
from mailings.models import Subscriber


class SubscribersXlsxConverter(XlsxConverter):
    MODEL = Subscriber
    FIELD_HEADER_MAP = {'id': 'Id', 'email': 'Email'}
    
    def __init__(self):
        super().__init__(self.FIELD_HEADER_MAP)
